
from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shopping.models import Product
import json

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)

    total_price = Decimal('0.0')
    items_with_totals = []
    for item in cart_items:
        try:
            price = Decimal(str(item.product.price).replace('Rp', '').replace('.', '').replace(',', '.'))
            item_total = price * item.quantity
            total_price += item_total
            items_with_totals.append({
                'item': item,
                'item_total': item_total
            })
        except InvalidOperation:
            return render(request, 'cart/view_cart.html', {
                'cart_items': items_with_totals,
                'total_price': total_price,
                'error': f"Invalid price format for {item.product}"
            })

    return render(request, 'cart/view_cart.html', {
        'cart_items': items_with_totals,
        'total_price': total_price,
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
            return JsonResponse({'success': True, 'new_quantity': cart_item.quantity})
        else:
            cart_item.delete()
            return JsonResponse({'success': True, 'deleted': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:view_cart')
