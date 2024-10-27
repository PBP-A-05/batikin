from django.shortcuts import redirect, render, get_object_or_404
from .models import Workshop, Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time

@login_required(login_url='register')
def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    return render(request, 'workshop_detail.html', {'workshop': workshop})

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
        current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()  # Contoh interval 30 menit
    return available_times

@login_required(login_url='register')
def workshop_book(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)

    # Misalkan Anda memiliki daftar waktu yang tersedia
    available_times = [time(hour=h) for h in range(9, 17)]  # Contoh jam dari 09:00 hingga 16:00

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        booking_time = request.POST.get('booking_time')  # Pastikan nama ini sesuai
        participants = int(request.POST.get('quantity', 1))

        if not selected_date:
            return render(request, 'workshop_book.html', {
                'workshop': workshop,
                'error': 'Please select a date',
                'available_times': available_times
            })

        booking = Booking(
            workshop=workshop,
            user=request.user,
            booking_time=booking_time,
            participants=participants,
            booking_date=selected_date
        )
        booking.save()

        return redirect('booking_success')

    return render(request, 'workshop_book.html', {
        'workshop': workshop,
        'available_times': available_times
    })