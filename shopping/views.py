from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
    data = [
        {
            'pk': str(product.pk),
            'fields': {
                'product_name': product.product_name,
                'price': product.price,
                'image_urls': product.image_urls,
                'category': product.category,
            }
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)

