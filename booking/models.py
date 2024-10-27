from django.db import models
from django.contrib.auth.models import User
import uuid

class Workshop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    open_time = models.CharField(max_length=50, default='')
    schedule = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    image_urls = models.TextField(default='')

    def __str__(self):
        return self.title

class Booking(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)  # Referensi ke model Workshop
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Referensi ke model User (yang sudah ada di Django)
    booking_date = models.DateField()  # Tanggal booking otomatis diisi saat booking
    booking_time = models.TimeField()  # Waktu booking
    participants = models.IntegerField(default=1)  # Jumlah peserta

    def __str__(self):
        return f'{self.user.username} - {self.workshop.title}'

class WorkshopProduct(models.Model):  # Mengganti nama kelas menjadi WorkshopProduct
    title = models.CharField(max_length=100)  # Nama produk workshop
    description = models.TextField()  # Deskripsi produk workshop
    def __str__(self):
        return self.title
    