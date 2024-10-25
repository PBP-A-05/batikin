from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
import json
from django.shortcuts import render
from pathlib import Path

def product_list(request):
    products = Product.objects.all()
    product_categories = Product.CATEGORY_CHOICES
    return render(request, 'shopping/templates/product_list.html', {
        'products': products,
        'product_categories': product_categories
    })

def product_detail(request, pk):  # Renamed parameter from 'product_id' to 'pk'
    product = get_object_or_404(Product, id=pk)  # Updated to use 'pk'
    return render(request, 'shopping/templates/product_detail.html', {'product': product})

def filter_products(request):
    category = request.GET.get('category')
    products = Product.objects.filter(category=category) if category else Product.objects.all()
    data = serializers.serialize('json', products)
    return HttpResponse(data, content_type='application/json')

from django.http import JsonResponse
from .models import Product
from django.views.decorators.http import require_POST
from wishlist.models import Wishlist

@require_POST
def like_product(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product = Product.objects.get(id=product_id)
    user = request.user

    product.like(user)

    wishlist_count = Wishlist.objects.filter(user=user).count()

    return JsonResponse({'success': True, 'wishlist_count': wishlist_count})


