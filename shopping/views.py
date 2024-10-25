from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist, Cart
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
import json

def product_list(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)
    product_categories = Product.CATEGORY_CHOICES
    
    if request.user.is_authenticated:
        for product in products:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    
    return render(request, 'shopping/templates/product_list.html', {
        'products': products,
        'product_categories': product_categories,
        'current_category': category
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'shopping/templates/product_detail.html', {'product': product, 'is_in_wishlist': is_in_wishlist})

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
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    message = f'{quantity} produk berhasil dimasukkan ke keranjang!'
    return JsonResponse({'message': message})

