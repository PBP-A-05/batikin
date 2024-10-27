from django.urls import path
from .views import workshop_detail, workshop_product_list, workshop_list, workshop_book
from . import views
urlpatterns = [
    path('workshop-products/', workshop_product_list, name='workshop_product_list'),
    path('workshops/<uuid:pk>/', views.workshop_detail, name='workshop_detail'),
    path('workshops/', views.workshop_list, name='workshop_list'),
    path('workshop-book/<uuid:pk>/', workshop_book, name='workshop_book'),
    path('api/get-bookings/', views.get_booking_data, name='get-bookings'),
]
