from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    addresses = models.ManyToManyField('Address')
    profile_picture = models.URLField(
        default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTOizmxkQV5rf4N9ayOC3pojndp0nzIDAFUtg&s",
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.address}"
