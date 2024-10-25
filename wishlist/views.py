from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from shopping.views import add_to_wishlist  
from shopping.models import Product, Wishlist  

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    wishlist_count = wishlist_items.count()

    return render(request, 'wishlist/templates/wishlist_view.html', {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
    })


@login_required
def add_to_wishlist_from_wishlist_app(request, product_id):
    return add_to_wishlist(request, product_id)


@login_required
def remove_from_wishlist(request, product_id):

    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    wishlist_item.delete()
    return redirect('wishlist_view')
