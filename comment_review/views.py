from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from comment_review.forms import ReviewForm
from comment_review.models import Review
from shopping.models import Product
from user_profile.models import Profile
from booking.models import Workshop

@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.rating = int(request.POST.get("rating", 0))
            review.review = request.POST.get("review", "")
            review.save()
            return JsonResponse({'redirect_url': reverse('product_detail', kwargs={'pk': product_id})})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': 'Form is invalid. Please correct the errors.', 'details': errors}, status=400)

    context = {
        'form': form,
        'product_name': product.product_name,
        'product_image_urls': product.image_urls,
        'id': product_id,
    }
    return render(request, "review_window.html", context)

@login_required
def edit_review(request, review_id, product_id):
    review = get_object_or_404(Review, pk=review_id)
    product = get_object_or_404(Product, id=product_id)

    if review.user != request.user:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

    form = ReviewForm(request.POST or None, instance=review)

    if request.method == "POST":
        if 'delete' in request.POST:
            return delete_review(request, review_id)
        elif form.is_valid():
            form.save()
            return JsonResponse({'redirect_url': reverse('product_detail', kwargs={'pk': product_id})})

    context = {
        'form': form,
        'review': review,
        'product_name': product.product_name,
        'product_image_urls': product.image_urls,
        'id': product_id,
    }
    return render(request, "edit_review.html", context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    product_id = review.product.id 

    if review.user == request.user:  
        review.delete()

    return redirect('product_detail', pk=product_id) 