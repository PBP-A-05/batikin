from django.shortcuts import render, redirect, get_object_or_404, reverse
from comment_review.forms import ProductEntryForm, ReviewForm
from comment_review.models import Product, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from comment_review.forms import ReviewForm
from comment_review.models import Review
from shopping.models import Product
from user_profile.models import Profile

@login_required
@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if 'cancel' in request.POST:
            return redirect('shopping:product_detail', product_id=product_id)

        elif 'submit' in request.POST and form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.rating = request.POST.get("rate", 0) 
            review.review = request.POST.get("review", "")
            review.save()

            return redirect('shopping:product_detail', product_id=product_id)

    context = {
        'form': form,
        'product_name': product.name,
        'product_image_url': product.image_urls[0] if product.image_urls else '',
    }
    return render(request, "review_window.html", context)

def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    form = ReviewForm(request.POST or None, instance=review)

    if request.method == "POST":
        if 'delete' in request.POST:
            return delete_review(request, review_id)

        elif 'submit' in request.POST and form.is_valid():
            form.save()
            return redirect('shopping:product_detail', product_id=review_id)

    context = {'form': form, 'review': review}
    return render(request, "edit_review.html", context)

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user == request.user:  
        review.delete()

    return redirect('product_detail', pk=product_id) 