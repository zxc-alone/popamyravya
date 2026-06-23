# api/views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from shop.models import Category, Product
from orders.models import Order

# Простые сериализаторы (временно)
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'size', 'color', 'available', 'image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# API для категорий
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# API для товаров
class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

# API для заказов (упрощенная версия)
class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()  # Добавлен queryset
    serializer_class = serializers.ModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Создаем сериализатор динамически
        class OrderSerializer(serializers.ModelSerializer):
            class Meta:
                model = Order
                fields = ['id', 'first_name', 'last_name', 'email', 'address', 
                         'postal_code', 'city', 'created', 'paid']
        return OrderSerializer
    
    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя
        if self.request.user.is_authenticated:
            return Order.objects.filter(email=self.request.user.email)
        return Order.objects.none()

# API для корзины (упрощенная версия)
class CartAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'items': [],
            'total_items': 0,
            'total_price': '0.00'
        })
    
    def post(self, request):
        return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_200_OK)

# API для аутентификации
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        # Простая регистрация
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username or not password:
            return Response({'error': 'Username и password обязательны'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь уже существует'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Вы успешно вышли'})

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)

# Корень API
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'T-Shirt Shop API v1',
        'endpoints': {
            'categories': '/api/categories/',
            'products': '/api/products/',
            'cart': '/api/cart/',
            'orders': '/api/orders/',
            'register': '/api/register/',
            'login': '/api/login/',
            'profile': '/api/profile/',
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    query = request.query_params.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query, available=True)[:20]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response([])