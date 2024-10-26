from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from shopping.models import Product
import json

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_items = cart.items.all()
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # Assuming 'price' is a field in Product

    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += quantity
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
