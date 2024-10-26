from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Profile, Address
from .forms import CombinedForm, ProfileForm, AddressForm
import os


@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    addresses = Address.objects.filter(user=user)
    
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': profile.phone_number,
    }
    form = CombinedForm(initial=initial_data)
    address_forms = [AddressForm(prefix=f'address_{i}', instance=addr) for i, addr in enumerate(addresses)]
    
    return render(request, 'account.html', {
        'form': form,
        'address_forms': address_forms,
        'addresses': addresses,
    })

@login_required
def pemesanan_view(request):
    return render(request, 'pemesanan.html')

@login_required
def booking_view(request):
    return render(request, 'booking.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form = CombinedForm(request.POST)
        
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()
            
            # Handle addresses
            addresses_data = []
            i = 0
            while f'address_{i}-title' in request.POST:
                title = request.POST.get(f'address_{i}-title')
                address = request.POST.get(f'address_{i}-address')
                if title and address:
                    addresses_data.append({
                        'title': title,
                        'address': address
                    })
                i += 1

            # Update addresses
            Address.objects.filter(user=request.user).delete()
            addresses = []
            for addr_data in addresses_data:
                address = Address.objects.create(
                    user=request.user,
                    title=addr_data['title'],
                    address=addr_data['address']
                )
                addresses.append({
                    'title': address.title,
                    'address': address.address
                })
            
            print("Updated addresses:", addresses)  # Debug print
            
            return JsonResponse({
                'status': 'success',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': profile.phone_number,
                'addresses': addresses,
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
