# api/urls.py (добавить в начало файла)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views


schema_view = get_schema_view(
    openapi.Info(
        title="T-Shirt Shop API",
        default_version='v1',
        description="API для интернет-магазина футболок",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@tshirtshop.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)



# Создание роутера для ViewSet
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    # Корень API
    path('', views.api_root, name='api-root'),
    
    # Включение маршрутов от роутера
    path('', include(router.urls)),
    
    # Корзина
    path('cart/', views.CartAPIView.as_view(), name='api-cart'),
    
    # Поиск
    path('search/', views.search_products, name='api-search'),
    
    # Аутентификация
    path('register/', views.RegisterAPIView.as_view(), name='api-register'),
    path('login/', views.LoginAPIView.as_view(), name='api-login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api-logout'),
    path('profile/', views.ProfileAPIView.as_view(), name='api-profile'),
    
    # Получение токена (альтернативный способ)
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
