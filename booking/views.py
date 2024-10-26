from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Workshop

def workshop_detail(request, pk):
    workshops = [
        {
            'id': '6fad6d3a-962e-4e1c-8cbb-6e8a7512381f', 
            'name': 'Kampung Batik Jogja Giriloyo',
            'address': 'Jl. Giriloyo, Karang Kulon, Wukirsari, Kecamatan Imogiri, Kabupaten Bantul',
            'time': '09.00-16.00',
            'image_urls': ['https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/jogjapos/2024/05/20221122_083254.jpg'],
            'website': 'https://example.com',
            'map_url': 'https://maps.google.com',
            'price': 'Rp. 100.000',
            'category': 'workshop',
            'additional_info': 'Deskripsi lengkap tentang workshop ini.'
        },
    ]
    return render(request, 'workshop_detail.html', {'workshop': workshops})

def workshop_list(request):
    workshops = [
        {
            'id': '6fad6d3a-962e-4e1c-8cbb-6e8a7512381f', 
            'name': 'Kampung Batik Jogja Giriloyo',
            'address': 'Jl. Giriloyo, Karang Kulon, Wukirsari, Kecamatan Imogiri, Kabupaten Bantul',
            'time': '09.00-16.00',
            'image_url': 'https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/jogjapos/2024/05/20221122_083254.jpg',
            'website': 'https://example.com',
            'map_url': 'https://maps.google.com',
        },
    ]
    return render(request, 'workshop_list.html', {'workshops': workshops})

def workshop_product_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshop_list.html', {'workshops': workshops})

def workshop_book(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)  # Asumsi Workshop adalah model Anda
    return render(request, 'workshop_book.html', {'workshop': workshop})
