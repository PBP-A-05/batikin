from django.shortcuts import render, get_object_or_404
from .models import Workshop

def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    return render(request, 'workshop_detail.html', {'workshop': workshop})

def workshop_list(request):
    workshops = Workshop.objects.all()  # Ambil semua workshop
    return render(request, 'booking/workshop_list.html', {'workshops': workshops})

def workshop_product_list(request):
    # Jika ada produk workshop, tambahkan logika di sini
    return render(request, 'workshop/workshop_list.html', {})
