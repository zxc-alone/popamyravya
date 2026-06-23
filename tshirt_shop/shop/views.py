from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product
from cart.cart import Cart

def home(request):
    """Главная страница"""
    featured_products = Product.objects.filter(available=True)[:6]
    new_products = Product.objects.filter(available=True).order_by('-created')[:6]
    
    context = {
        'featured_products': featured_products,
        'new_products': new_products,
    }
    return render(request, 'shop/home.html', context)

def product_list(request, category_slug=None):
    """Список товаров"""
    category = None
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Фильтрация по размеру и цвету
    size = request.GET.get('size')
    color = request.GET.get('color')
    
    if size:
        products = products.filter(size=size)
    if color:
        products = products.filter(color=color)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'shop/product_detail.html', context)

def cart_detail(request):
    """Корзина покупок"""
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def cart_add(request, product_id):
    """Добавление в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'{product.name} добавлен в корзину!')
    
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    """Удаление из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'{product.name} удален из корзины')
    
    return redirect('shop:cart_detail')