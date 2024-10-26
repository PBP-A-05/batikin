from django.contrib import admin
from django.urls import include, path
from batikin.views import home_view
from user_profile.views import profile_view, update_profile
from django.urls import path
from user_profile.views import profile_view

urlpatterns = [
    path('', profile_view, name='account'),
    path('update/', update_profile, name='update_profile'),
]
