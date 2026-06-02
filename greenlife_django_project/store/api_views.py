from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Sum, F
from .models import Category, Plant, Order, Article, Cart, CartItem
from .serializers import (
    CategorySerializer, PlantSerializer, OrderSerializer, 
    ArticleSerializer, UserSerializer, CartSerializer, CartItemSerializer
)

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return Cart.objects.filter(id=cart.id)

    def list(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        plant_id = request.data.get('plant_id')
        quantity = int(request.data.get('quantity', 1))
        
        item, created = CartItem.objects.get_or_create(cart=cart, plant_id=plant_id)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        plant_id = request.data.get('plant_id')
        quantity = int(request.data.get('quantity', 0))
        
        try:
            item = CartItem.objects.get(cart=cart, plant_id=plant_id)
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()
        except CartItem.DoesNotExist:
            pass
            
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class ShopStatsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        totals = Plant.objects.aggregate(
            total_plants=Count('id'),
            avg_price=Avg('price'),
            total_stock_value=Sum(F('price'))
        )
        popular_plants = Plant.objects.annotate(
            order_count=Count('order_items')
        ).order_by('-order_count')[:5]
        
        revenue_by_plant = Plant.objects.annotate(
            revenue=Sum(F('order_items__price') * F('order_items__quantity'))
        ).order_by('-revenue')[:5]

        categories_stats = Category.objects.annotate(
            num_plants=Count('plants')
        ).values('name', 'num_plants').order_by('-num_plants')

        authors = Article.objects.values_list('author', flat=True).distinct()
        active_articles_count = Article.objects.filter(is_active=True).count()
        
        return Response({
            'stats': totals,
            'popular': PlantSerializer(popular_plants, many=True, context={'request': request}).data,
            'revenue': [
                {'name': p.name, 'revenue': p.revenue or 0} for p in revenue_by_plant
            ],
            'categories': list(categories_stats),
            'authors': list(authors),
            'active_articles': active_articles_count
        })

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PlantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plant.available_plants.available().select_related('category')
    serializer_class = PlantSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        search = self.request.query_params.get('q')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items__plant')
    serializer_class = OrderSerializer
