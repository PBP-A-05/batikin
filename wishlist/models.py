import uuid
from django.db import models
from django.contrib.auth.models import User
from shopping.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

