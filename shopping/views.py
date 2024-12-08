from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from wishlist.models import Wishlist
from cart.models import Cart, CartItem
from comment_review.models import Review
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
import json
from django.http import HttpResponse
from django.core import serializers
from .models import Product
import uuid

def product_list(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)
    product_categories = Product.CATEGORY_CHOICES
    
    wishlist_products = []
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    return render(request, 'shopping/product_list.html', {
        'products': products,
        'product_categories': product_categories,
        'current_category': category,
        'wishlist_products': list(map(str, wishlist_products))  
    })
    
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    reviews = Review.objects.filter(product=product)
    return render(request, 'shopping/product_detail.html', {'product': product, 'is_in_wishlist': is_in_wishlist, 'reviews': reviews})

def product_detail_check(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    return HttpResponse(status=200)

def filter_products(request):
    category = request.GET.get('category')
    products = Product.objects.filter(category=category) if category else Product.objects.all()
    
    data = [
        {
            'id': str(product.id),
            'product_name': product.product_name,
            'price': str(product.price),
            'image_urls': product.image_urls,
            'category': product.category,
            'category_display': product.get_category_display(),
            'is_in_wishlist': Wishlist.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        message = 'Produk ditambahkan ke wishlist!'
        status = 'added'
    else:
        Wishlist.objects.filter(user=request.user, product=product).delete()
        message = 'Produk dihapus dari wishlist!'
        status = 'removed'
    
    return JsonResponse({'message': message, 'status': status})

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

def get_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        'id': str(product.id),
        'product_name': product.product_name,
        'price': str(product.price),
        'image_urls': product.image_urls,
        'category': product.category,
        'category_display': product.category,
    })

def show_json(request):
    data = Product.objects.all()  # Mengambil semua produk
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)  # Mengambil produk berdasarkan ID
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")