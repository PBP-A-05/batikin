from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Workshop, Booking
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from django.core.exceptions import ObjectDoesNotExist
from comment_review.models import Review

@login_required(login_url='register')
def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    reviews = Review.objects.filter(workshop=workshop)
    return render(request, 'workshop_detail.html', {'workshop': workshop, 'reviews': reviews})

def workshop_list(request):
    sort = request.GET.get('sort')
    if sort == 'alphabet':
        workshops = Workshop.objects.all().order_by('title')
    else:
        workshops = Workshop.objects.all()
    context = {'workshops': workshops}
    return render(request, 'workshop_list.html', context)

def workshop_product_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshop_list.html', {'workshops': workshops})

def generate_available_times(open_time, close_time):
    # Fungsi ini harus disesuaikan dengan logika Anda untuk menghasilkan waktu yang tersedia
    available_times = []
    current_time = open_time
    while current_time <= close_time:
        available_times.append(current_time.strftime("%H:%M"))
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()  # Example 30-minute intervals
    return available_times

@login_required(login_url='register')
def workshop_book(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)

    # Define available times (e.g., from 09:00 to 16:30 in 30-minute intervals)
    open_time = time(hour=9, minute=0)
    close_time = time(hour=16, minute=30)
    available_times = generate_available_times(open_time, close_time)

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        booking_time_str = request.POST.get('booking_time')  # Ensure this name matches the form
        participants = request.POST.get('participants')

        # Validate the selected_date
        if not selected_date:
            return render(request, 'workshop_book.html', {
                'workshop': workshop,
                'error': 'Please select a date.',
                'available_times': available_times
            })

        if not booking_time_str:
            return render(request, 'workshop_book.html', {
                'workshop': workshop,
                'error': 'Please select a booking time.',
                'available_times': available_times
            })

        try:
            booking_time = datetime.strptime(booking_time_str, '%H:%M').time()
        except ValueError:
            return render(request, 'workshop_book.html', {
                'workshop': workshop,
                'error': 'Invalid booking time format.',
                'available_times': available_times
            })

        try:
            participants = int(participants)
            if participants < 1:
                raise ValueError
        except ValueError:
            return render(request, 'workshop_book.html', {
                'workshop': workshop,
                'error': 'Number of participants must be at least 1.',
                'available_times': available_times
            })

        booking = Booking(
            workshop=workshop,
            user=request.user,
            booking_date=selected_date,
            booking_time=booking_time,
            participants=participants
        )
        booking.save()
    return render(request, 'workshop_book.html', {
        'workshop': workshop,
        'available_times': available_times
    })

@login_required(login_url='register')
def get_booking_data(request):
    try:
        print("Fetching bookings for user:", request.user)  # Debug print
        bookings = Booking.objects.filter(user=request.user).select_related('workshop')
        print("Found bookings:", bookings.count())  # Debug print
        
        booking_data = []
        for booking in bookings:
            try:
                booking_data.append({
                    'workshop_title': booking.workshop.title,
                    'location': booking.workshop.location,
                    'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
                    'booking_time': booking.booking_time.strftime('%H:%M'),
                    'participants': booking.participants,
                })
                print("Processed booking:", booking.id)  
            except AttributeError as e:
                print(f"Error processing booking {booking.id}: {str(e)}")
                continue
        
        return JsonResponse({
            'status': 'success',
            'bookings': booking_data
        })
        
    except Exception as e:
        print("Error in get_booking_data:", str(e))  
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred while fetching bookings',
            'error': str(e)
        }, status=500)