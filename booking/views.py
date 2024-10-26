from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Workshop, Wishlist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    return render(request, 'workshop_detail.html', {'workshop': workshop})

def workshop_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshop_list.html', {'workshops': workshops})

def workshop_product_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshop_list.html', {'workshops': workshops})

def workshop_book(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)  # Asumsi Workshop adalah model Anda
    return render(request, 'workshop_book.html', {'workshop': workshop})

@login_required
def add_to_wishlist(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    Wishlist, created = Wishlist.objects.get_or_create(user=request.user, workshop=workshop)
    
    if created:
        message = 'Workshop ditambahkan ke wishlist!'
        status = 'added'
    else:
        Wishlist.objects.filter(user=request.user, workshop=workshop).delete()
        message = 'Workshop dihapus dari wishlist!'
        status = 'removed'
    
    return JsonResponse({'message': message, 'status': status})
