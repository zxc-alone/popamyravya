# api/serializers.py
from rest_framework import serializers
from shop.models import Category, Product
from orders.models import Order, OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    products_count = serializers.IntegerField(source='products.count', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'products_count']
        read_only_fields = ['id', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    color_display = serializers.CharField(source='get_color_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'size', 'size_display', 'color', 'color_display',
            'category', 'category_name', 'category_id',
            'available', 'image', 'image_url',
            'created', 'updated'
        ]
        read_only_fields = ['id', 'slug', 'created', 'updated']
    
    def get_image_url(self, obj):
        """Получение полного URL изображения"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class ProductListSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для списка товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category_name', 'image_url', 'available']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции заказа"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_id', 'price', 'quantity', 'get_cost']
        read_only_fields = ['id', 'price']

class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа"""
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.DecimalField(source='get_total_cost', max_digits=10, decimal_places=2, read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email', 'address',
            'postal_code', 'city', 'created', 'updated', 'paid',
            'items', 'total_cost', 'status_display'
        ]
        read_only_fields = ['id', 'created', 'updated']

    def get_status_display(self, obj):
        return "Оплачен" if obj.paid else "Не оплачен"

class CreateOrderSerializer(serializers.Serializer):
    """Сериализатор для создания заказа из корзины"""
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=250)
    postal_code = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=100)

class CartItemSerializer(serializers.Serializer):
    """Сериализатор для элемента корзины"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=99)
    product_name = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

class CartSerializer(serializers.Serializer):
    """Сериализатор для корзины"""
    items = CartItemSerializer(many=True)
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)