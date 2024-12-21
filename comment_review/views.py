from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from comment_review.forms import ReviewForm
from comment_review.models import Review
from shopping.models import Product
from user_profile.models import Profile
from booking.models import Workshop
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from uuid import UUID
import json

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

@csrf_exempt
def edit_review(request, review_id, product_id):
    try:
        review = get_object_or_404(Review, pk=review_id)
        product = get_object_or_404(Product, id=product_id)

        if review.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

        if request.method == "POST":
            data = json.loads(request.body)
            review.rating = int(data.get('rating'))
            review.review = data.get('review')
            review.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Review updated successfully'
            })

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
def delete_review(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        
        if review.user == request.user:
            review.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Review deleted successfully'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Unauthorized'
            }, status=403)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def show_json(request):
    data = Product.objects.all()  # Mengambil semua produk
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    try:
        reviews = Review.objects.filter(product_id=id)
        data = serializers.serialize('json', reviews)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_product_reviews(request, product_id):
    try:
        reviews = Review.objects.filter(product_id=product_id).select_related('user')
        review_data = []
        for review in reviews:
            review_dict = {
                'model': 'comment_review.review',
                'pk': str(review.id),
                'fields': {
                    'user': review.user.username,  # Get username instead of ID
                    'product': str(review.product.id),
                    'profile_pic': review.profile_pic,
                    'rating': review.rating,
                    'review': review.review,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat(),
                }
            }
            review_data.append(review_dict)
        return JsonResponse(review_data, safe=False)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Add debug logging
            print(f"Received data: {data}")
            
            new_review = Review.objects.create(
                user=request.user,
                product=Product.objects.get(pk=data["product_id"]),
                rating=int(data["rating"]),
                review=data["review"]
            )
            
            return JsonResponse({
                "status": "success",
                "message": "Review created successfully"
            })
            
        except json.JSONDecodeError as e:
            return JsonResponse({
                "status": "error",
                "message": f"Invalid JSON: {str(e)}"
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    
    return JsonResponse({
        "status": "error",
        "message": "Only POST method is allowed"
    }, status=405)