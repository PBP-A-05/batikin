
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from .models import Cart, CartItem, Order, OrderItem
from shopping.models import Product
from user_profile.models import Address
import json

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    
    total_price = Decimal('0.0')
    total_quantity = 0
    items_with_totals = []

    for item in cart_items:
        try:
            price = Decimal(str(item.product.price).replace('Rp', '').replace('.', '').replace(',', '.'))
            item_total = price * item.quantity
            total_price += item_total
            total_quantity += item.quantity  
            items_with_totals.append({
                'item': item,
                'item_total': item_total
            })
        except InvalidOperation:
            return render(request, 'cart/view_cart.html', {
                'cart_items': items_with_totals,
                'total_price': total_price,
                'total_quantity': total_quantity,
                'error': f"Invalid price format for {item.product}"
            })

    return render(request, 'cart/view_cart.html', {
        'cart_items': items_with_totals,
        'total_price': total_price,
        'total_quantity': total_quantity,  
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 1))
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    message = f'{quantity} produk berhasil dimasukkan ke keranjang!'
    return JsonResponse({'message': message})

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            new_total = cart_item.quantity * cart_item.price
            return JsonResponse({'success': True, 'new_quantity': cart_item.quantity, 'new_total': new_total})
        else:
            cart_item.delete()
            return JsonResponse({'success': True, 'deleted': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
@require_POST
def create_order(request):
    data = json.loads(request.body)
    address_id = data.get('address_id')
    items = data.get('items')

    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Alamat tidak ditemukan'})

    total_price = sum(item['price'] * item['quantity'] for item in items)

    order = Order.objects.create(
        user=request.user,
        address=address,
        total_price=total_price
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )

    # Clear the user's cart here

    return JsonResponse({'status': 'success', 'message': 'Pesanan berhasil dibuat'})
