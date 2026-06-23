# tshirt_shop/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Временно закомментируйте эти строки
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    
    # API маршруты
    path('api/', include('api.urls')),
    
    # Документация API - временно закомментируйте
    # path('api/docs/', include_docs_urls(title='T-Shirt Shop API')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)