from django.contrib import admin
from django.urls import include, path
from batikin.views import home_view
from user_profile.views import profile_view, update_profile, pemesanan_view, booking_view
from django.urls import path
from user_profile.views import profile_view

urlpatterns = [
    path('account/', profile_view, name='profile'),
    path('pemesanan/', pemesanan_view, name='pemesanan'),
    path('booking/', booking_view, name='booking'),
    path('update/', update_profile, name='update_profile'),
]
