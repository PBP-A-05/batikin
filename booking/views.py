from django.shortcuts import redirect, render, get_object_or_404
from .models import Workshop, Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required(login_url='register')
@login_required
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

def workshop_book(request, pk):
    # Ambil objek Workshop berdasarkan ID
    workshop = get_object_or_404(Workshop, pk=pk)
    
    # Pecah jadwal menjadi daftar waktu terpisah
    available_times = workshop.schedule.split(', ')
    
    context = {
        'workshop': workshop,
        'available_times': available_times,
    }
    
    return render(request, 'workshop_book.html', context)

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

    if request.method == 'POST':
        # Ambil data dari form
        selected_date = request.POST.get('selected_date')  # Pastikan Anda mendapatkan tanggal yang dipilih
        time = request.POST.get('time')
        participants = int(request.POST.get('quantity', 1))

        # Validasi jika tanggal belum dipilih
        if not selected_date:
            # Anda bisa menambahkan error handling di sini
            return render(request, 'workshop_book.html', {'workshop': workshop, 'error': 'Please select a date'})

        # Buat instance booking
        booking = Booking(
            workshop=workshop,
            user=request.user,
            booking_time=time,
            participants=participants,
            date=selected_date  # Simpan tanggal yang dipilih
        )
        booking.save()

        return redirect('booking_success')  # Redirect ke halaman konfirmasi

    # Jika bukan POST, render form booking
    return render(request, 'workshop_book.html', {'workshop': workshop})