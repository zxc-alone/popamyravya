# api/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from shop.models import Category, Product

class ProductAPITestCase(APITestCase):
    def setUp(self):
        # Создание тестовых данных
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.product = Product.objects.create(
            category=self.category,
            name='Test T-Shirt',
            slug='test-tshirt',
            price=1000,
            size='M',
            color='white',
            available=True
        )
    
    def test_get_products(self):
        """Тест получения списка товаров"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_product_detail(self):
        """Тест получения деталей товара"""
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test T-Shirt')