from django.urls import path
from . import views

urlpatterns = [
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/count/', views.wishlist_count, name='wishlist_count'),
]
