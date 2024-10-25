import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('pakaian_pria', 'Pakaian Pria'),
        ('pakaian_wanita', 'Pakaian Wanita'),
        ('aksesoris', 'Aksesoris'),
        ('workshop', 'Workshop'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store_url = models.URLField(max_length=200)
    store_address = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    image_urls = models.JSONField()
    additional_info = models.TextField()
    product_link = models.URLField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.product_name
    