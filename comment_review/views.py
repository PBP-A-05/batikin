from django.shortcuts import render, redirect, get_object_or_404, reverse
from comment_review.forms import ProductEntryForm
from comment_review.models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def create_review(request, product_id):
    form = ProductEntryForm(request.POST or None)
    product = get_object_or_404(Product.objects.using('product_db'), id=product_id) # Bagaimana cara buat masukkin db nya????????

    if request.method == "POST":
        if 'cancel' in request.POST:
            return redirect('shopping:product_detail', product_id=product_id)

        elif 'submit' in request.POST and form.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.product = product
            product_entry.rating = request.POST.get("rate", 0)
            product_entry.review = request.POST.get("review", "")
            product_entry.save()

            return redirect('shopping:product_detail', product_id=product_id)

    context = {
        'form': form,
        'name': product.product_name,
        'image_url': product.image_urls[0] if product.image_urls else '',
    }
    return render(request, "review_window", context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = ProductEntryForm(request.POST or None, instance=product)

    if request.method == "POST":
        if 'cancel' in request.POST:
            return redirect('shopping:product_detail', product_id=product_id)

        elif 'submit' in request.POST and form.is_valid():
            form.save()
            return redirect('shopping:product_detail', product_id=product_id)

    context = {'form': form, 'product': product}
    return render(request, "edit_review.html", context)