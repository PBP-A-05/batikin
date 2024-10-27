"""
URL configuration for batikin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from batikin.views import home_view, login_view, register_view
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_view, name='home'),  # Home page, extending base.html
    path('account/', include('user_profile.urls', namespace='user_profile')),  # Include user_profile URLs
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('shopping/', include('shopping.urls')),
    path('workshop/', include('booking.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('cart/', include('cart.urls')),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('booking/', include('booking.urls')),  # Ensure this line is present
]
