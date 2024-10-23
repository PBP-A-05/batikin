from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    category = request.GET.get('category', 'all')
    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)
    return render(request, 'shopping/templates/product_list.html', {'products': products, 'selected_category': category})

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'shopping/templates/product_detail.html', {'product': product})

def product_detail(request):
    # sementara
    return render(request, 'shopping/templates/product_detail.html')