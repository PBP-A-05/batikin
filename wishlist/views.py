from decimal import Decimal
import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Wishlist  
from shopping.models import Product  
from django.db.models import F
from django.db.models import DecimalField, ExpressionWrapper, FloatField
from django.db.models.functions import Cast

@login_required(login_url='/login')
def wishlist_view(request):
    sort_by = request.GET.get('sort', 'price_asc')  

    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    wishlist_items = wishlist_items.annotate(
        price_decimal=Cast('product__price', output_field=DecimalField())
    )

    if sort_by == 'price_desc':
        wishlist_items = wishlist_items.order_by('-price_decimal')
    else:  
        wishlist_items = wishlist_items.order_by('price_decimal')

    wishlist_count = wishlist_items.count()

    return render(request, 'wishlist/wishlist_view.html', {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
    })


@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            message = 'Produk ditambahkan ke wishlist!'
            status = 'added'
        else:
            wishlist.delete()
            message = 'Produk dihapus dari wishlist!'
            status = 'removed'
        
        return JsonResponse({'message': message, 'status': status})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist = Wishlist.objects.filter(user=request.user, product=product)

        if wishlist.exists():
            wishlist.delete()
            message = 'Produk berhasil dihapus dari wishlist!'
            success = True
        else:
            message = 'Produk tidak ditemukan di wishlist.'
            success = False
        
        return JsonResponse({'success': success, 'message': message})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 1))

    try:
        price = Decimal(str(product.price).replace('Rp', '').replace('.', '').replace(',', '.'))
    except:
        return JsonResponse({'error': 'Invalid price format'}, status=400)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity, 'price': price}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    message = f'{quantity} produk berhasil dimasukkan ke keranjang!'
    return JsonResponse({'message': message})


@login_required
def remove_from_cart(request, product_id):
    try:

        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
        cart_item.delete()
        message = 'Produk dihapus dari keranjang!'
        return JsonResponse({'status': 'removed', 'message': message})
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found in cart.'}, status=404)
    
@login_required
def save_note(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        note_text = request.POST.get('note', '')
        wishlist_item.note = note_text
        wishlist_item.save()

        return JsonResponse({'message': 'Catatan berhasil disimpan!', 'note': wishlist_item.note})

    return JsonResponse({'error': 'Invalid request method'}, status=400)