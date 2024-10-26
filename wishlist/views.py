from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist  
from shopping.models import Product  

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
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
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    wishlist_item.delete()
    return redirect('wishlist_view')
