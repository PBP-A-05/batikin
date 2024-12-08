import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
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
    
    open_modal = request.GET.get('open_modal', 'false').lower() in ['true', '1', 'yes']


    return render(request, 'account.html', {
        'form': form,
        'address_forms': address_forms,
        'addresses': addresses,
        'open_modal': open_modal,
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

@login_required
def get_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    address_data = [{'id': addr.id, 'title': addr.title, 'address': addr.address} for addr in addresses]
    return JsonResponse({'addresses': address_data})

@login_required
def get_user_info(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    addresses = Address.objects.filter(user=user).values('id', 'title', 'address')
    addresses_list = list(addresses)
    
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': profile.phone_number,
        'username': user.username,
        'addresses': addresses_list,
    }
    
    return JsonResponse(data)

@csrf_exempt
@login_required
def update_user_info(request):
    if request.method == 'POST':
        # Determine content type
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"status": False, "message": "Invalid JSON."}, status=400)
        else:
            data = request.POST

        # Extract fields
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')

        # Validate fields
        errors = {}
        if not first_name:
            errors['first_name'] = "First name is required."
        if not last_name:
            errors['last_name'] = "Last name is required."
        if not phone_number:
            errors['phone_number'] = "Phone number is required."

        if errors:
            return JsonResponse({"status": False, "errors": errors}, status=400)

        # Update User and Profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone_number = phone_number
        profile.save()

        return JsonResponse({
            'status': 'success',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': profile.phone_number,
        }, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)