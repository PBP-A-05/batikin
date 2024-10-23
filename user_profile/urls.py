from django.contrib import admin
from django.urls import include, path
from batikin.views import home_view
from user_profile.views import profile_view
from django.urls import path
from user_profile.views import profile_view

urlpatterns = [
    path('', profile_view, name='account'),
]