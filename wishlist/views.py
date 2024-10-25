from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from shopping.models import Product
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt


def view_wishlist(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    product_count = products.count()  

    return render(request, 'wishlist/wishlist.html', {
        'products': products,
        'product_count': product_count
    })


@csrf_exempt
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, id=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)

    # Debugging print
    print(f"Added {product.name} to wishlist for user {request.user.username}")

    return JsonResponse({'status': 'added'})


@csrf_exempt
def remove_from_wishlist(request, pk):
    product = get_object_or_404(Product, id=pk)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return JsonResponse({'status': 'removed'})

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        return JsonResponse({'count': wishlist.products.count()})
    return JsonResponse({'count': 0})

