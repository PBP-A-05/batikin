from django.shortcuts import render, get_object_or_404
from .models import Workshop

def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    return render(request, 'workshop_detail.html', {'workshop': workshop})

def workshop_list(request):
    workshops = [
        {
            'id': 1,
            'name': 'Kampung Batik Jogja Giriloyo',
            'address': 'Jl. Giriloyo, Karang Kulon, Wukirsari, Kecamatan Imogiri, Kabupaten Bantul',
            'time': '09.00-16.00',
            'image_url': 'https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/jogjapos/2024/05/20221122_083254.jpg',
            'website': 'https://example.com',
            'map_url': 'https://maps.google.com',
        },
    ]
    return render(request, 'booking/workshop_list.html', {'workshops': workshops})

def workshop_product_list(request):
    workshops = Workshop.objects.all()  # Misalnya ambil data yang sama dulu
    return render(request, 'workshop/workshop_list.html', {'workshops': workshops})
