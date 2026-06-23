from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem

def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
    if request.method == 'POST':
        # Создание заказа
        order = Order.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            postal_code=request.POST['postal_code'],
            city=request.POST['city'],
        )
        
        # Создание позиций заказа
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        # Очистка корзины
        cart.clear()
        messages.success(request, 'Заказ успешно оформлен!')
        return redirect('shop:home')
    
    return render(request, 'orders/order_create.html', {'cart': cart})