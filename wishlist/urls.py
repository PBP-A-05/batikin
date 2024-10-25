from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist_view'),
    path('add_to_wishlist/<uuid:product_id>/', views.add_to_wishlist_from_wishlist_app, name='add_to_wishlist_from_wishlist_app'),
    path('remove_from_wishlist/<uuid:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
