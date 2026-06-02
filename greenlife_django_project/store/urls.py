from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import api_views

app_name = 'store'

router = DefaultRouter()
router.register(r'plants', api_views.PlantViewSet, basename='plant')
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'orders', api_views.OrderViewSet, basename='order')
router.register(r'articles', api_views.ArticleViewSet, basename='article')
router.register(r'cart', api_views.CartViewSet, basename='cart')

urlpatterns = [
    path('api/shop-stats/', api_views.ShopStatsView.as_view(), name='shop-stats'),
    path('api/', include(router.urls)),
    path('api/auth/register/', api_views.UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', obtain_auth_token, name='login'),
    path('api/auth/me/', api_views.UserDetailView.as_view(), name='me'),
    path('', views.plant_list, name='plant_list'),
    path('stats/', views.stats_view, name='stats'),
    path('new/', views.new_arrivals_view, name='new_arrivals'),
    path('search/', views.plant_list, name='plant_search'),
    path('<slug:category_slug>/', views.plant_list, name='plant_list_by_category'),
    path('<int:id>/<slug:slug>/', views.plant_detail, name='plant_detail'),
]
