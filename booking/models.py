from django.db import models
from django.contrib.auth.models import User

class Workshop(models.Model):
    title = models.CharField(max_length=100)  # Nama workshop
    location = models.CharField(max_length=200)  # Lokasi workshop
    description = models.TextField()  # Deskripsi workshop
    schedule = models.CharField(max_length=50)  # Jadwal waktu
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Rating workshop
    image = models.ImageField(upload_to='workshops/', null=True, blank=True)  # Gambar workshop

    def __str__(self):
        return self.title

class Booking(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)  # Referensi ke model Workshop
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Referensi ke model User (yang sudah ada di Django)
    booking_date = models.DateField(auto_now_add=True)  # Tanggal booking otomatis diisi saat booking
    booking_time = models.TimeField()  # Waktu booking
    participants = models.IntegerField(default=1)  # Jumlah peserta

    def __str__(self):
        return f'{self.user.username} - {self.workshop.title}'

class WorkshopProduct(models.Model):  # Mengganti nama kelas menjadi WorkshopProduct
    title = models.CharField(max_length=100)  # Nama produk workshop
    description = models.TextField()  # Deskripsi produk workshop
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Harga produk workshop
    stock = models.IntegerField(default=0)  # Stok produk workshop

    def __str__(self):
        return self.title
