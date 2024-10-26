from django.urls import path
from .views import workshop_detail, workshop_product_list, workshop_list, workshop_book
from . import views

urlpatterns = [
    path('workshop-products/', workshop_product_list, name='workshop_product_list'),
    path('<uuid:pk>/', workshop_detail, name='workshop_detail'),
    path('workshops/<uuid:pk>/', views.workshop_detail, name='workshop_detail'),
    path('workshops/', workshop_list, name='workshop_list'),
    path('workshops/', views.workshop_list, name='workshop_list'),
    path('workshop-book/<uuid:pk>/', workshop_book, name='workshop_book'),
    path('wishlist/add/<uuid:workshop_id>/', views.add_to_wishlist, name='add_to_wishlist'),
]
