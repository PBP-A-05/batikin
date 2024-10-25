from django.contrib.auth import get_user_model
from django.db import models
from shopping.models import Product 

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='wishlists')  

    def __str__(self):
        return f"{self.user.username}'s wishlist"
