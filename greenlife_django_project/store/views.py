from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Avg, Sum, F
from .models import Category, Plant, Order, Article
from django.utils import timezone
from datetime import timedelta

def plant_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    plants = Plant.available_plants.available()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        plants = plants.filter(category=category)
    
    query = request.GET.get('q')
    if query:
        plants = plants.filter(name__icontains=query) | plants.filter(description__contains=query)

    total_found = plants.count()
    plants = plants.exclude(price__lt=5)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        plants = plants.order_by('price')
    elif sort == 'price_desc':
        plants = plants.order_by('-price')

    return render(request,
                  'store/plant_list.html',
                  {'category': category,
                   'categories': categories,
                   'plants': plants,
                   'total_found': total_found
                   })


def plant_detail(request, id, slug):
    plant_qs = Plant.objects.filter(id=id, slug=slug, is_in_stock=True)
    if not plant_qs.exists():
        return redirect('store:plant_list')
    plant = plant_qs.first()
    return render(request, 'store/plant_detail.html', {'plant': plant})

def stats_view(request):
    total_plants = Plant.objects.count()
    total_value = Plant.objects.aggregate(total=Sum('price'))
    avg_price = Plant.objects.aggregate(average_price=Avg('price'))
    
    plants_by_popularity = Plant.objects.annotate(
        times_ordered=Count('order_items')
    ).order_by('-times_ordered')

    plants_with_revenue = Plant.objects.annotate(
        revenue=Sum(F('order_items__price') * F('order_items__quantity'))
    ).order_by('-revenue')

    categories_with_plant_count = Category.objects.annotate(
        num_plants=Count('plants')
    ).order_by('-num_plants')

    context = {
        'total_plants': total_plants,
        'total_value': total_value,
        'avg_price': avg_price,
        'plants_by_popularity': plants_by_popularity,
        'plants_with_revenue': plants_with_revenue,
        'categories_with_plant_count': categories_with_plant_count,
    }
    return render(request, 'store/stats.html', context)

def new_arrivals_view(request):
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    new_plants = Plant.objects.filter(created_at__gte=seven_days_ago)
    today = now.date()
    delivery_today = Order.objects.filter(delivery_date=today)
    published_articles = Article.objects.filter(published_at__lte=now, is_active=True)
    
    context = {
        'new_plants': new_plants,
        'delivery_today': delivery_today,
        'published_articles': published_articles,
    }
    return render(request, 'store/new_arrivals.html', context)
