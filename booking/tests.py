from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from booking.models import Workshop, Booking
from django.contrib.auth.models import User

class WorkshopBookingTestCase(TestCase):
    def setUp(self):
        # Buat pengguna
        self.user = User.objects.create_user(username='testuser', password='password')

        # Buat workshop
        self.workshop = Workshop.objects.create(
            title="Kampung Batik Jogja Giriloyo",
            location="Jl. Giriloyo, Karang Kulon, Wukirsari, Kecamatan Imogiri, Kabupaten Bantul",
            description="Workshop batik tradisional di Jogja",
            open_time="09.00-16.00",
            schedule="Setiap hari",
            rating=4.5,
            image_urls="https://static.promediateknologi.id/crop/0x0:0x0/0x0/webp/photo/jogjapos/2024/05/20221122_083254.jpg"
        )

    def test_workshop_list_view(self):
        """Test untuk memastikan view workshop list berfungsi dengan benar"""
        response = self.client.get(reverse('workshop_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.workshop.title)

    def test_workshop_detail_view(self):
        """Test untuk memastikan view workshop detail berfungsi dengan benar"""
        self.client.login(username='testuser', password='password')  # Tambahkan login
        response = self.client.get(reverse('workshop_detail', kwargs={'pk': self.workshop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.workshop.description)

    def test_workshop_booking_view(self):
        """Test untuk memastikan booking workshop berhasil"""
        # Login user
        self.client.login(username='testuser', password='password')

        # Data booking yang benar
        booking_data = {
            'selected_date': timezone.now().date(),  # Pastikan nama field sesuai
            'booking_time': '09:00',  # Format waktu sesuai dengan TimeField
            'participants': 3
        }

        # Arahkan ke view booking
        response = self.client.post(reverse('workshop_book', kwargs={'pk': self.workshop.id}), data=booking_data)

        # Pastikan status booking berhasil (redirect)
        self.assertEqual(response.status_code, 302)

        # Cek apakah booking berhasil disimpan
        booking = Booking.objects.get(workshop=self.workshop, user=self.user)
        self.assertEqual(booking.participants, 3)

    def test_booking_with_invalid_time_format(self):
        """Test untuk memastikan jika waktu yang salah memberikan error"""
        self.client.login(username='testuser', password='password')

        booking_data = {
            'selected_date': timezone.now().date(),
            'booking_time': 'invalid_time',  # Format waktu yang tidak valid
            'participants': 3
        }

        response = self.client.post(reverse('workshop_book', kwargs={'pk': self.workshop.id}), data=booking_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid booking time format.')  # Pastikan pesan error muncul

    def test_booking_with_no_participants(self):
        """Test untuk memastikan bahwa tidak bisa memesan tanpa peserta"""
        self.client.login(username='testuser', password='password')

        booking_data = {
            'selected_date': timezone.now().date(),
            'booking_time': '09:00',
            'participants': 0  # Jumlah peserta tidak valid
        }

        response = self.client.post(reverse('workshop_book', kwargs={'pk': self.workshop.id}), data=booking_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Number of participants must be at least 1.')  # Pastikan pesan error muncul
