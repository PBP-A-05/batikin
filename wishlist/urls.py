from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist_view'),
    path('add/<uuid:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<uuid:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
