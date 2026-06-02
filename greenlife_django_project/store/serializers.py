from rest_framework import serializers
from .models import Category, Plant, Order, OrderItem, Article, Tag, Cart, CartItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'author', 'published_at', 'image']

class PlantSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Plant
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'is_in_stock', 'image', 'published_at', 'articles', 'tags']

class CartItemSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(read_only=True)
    plant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'plant', 'plant_id', 'quantity', 'get_cost']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'get_total_price']

class OrderItemSerializer(serializers.ModelSerializer):
    plant_id = serializers.IntegerField(write_only=True)
    plant = PlantSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'plant_id', 'plant', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_email', 'phone', 'address', 'city',
            'status', 'created_at', 'updated_at', 'delivery_date', 'items', 'get_total_cost'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            plant_id = item_data.pop('plant_id')
            plant = Plant.objects.get(id=plant_id)
            OrderItem.objects.create(order=order, plant=plant, **item_data)
        return order
