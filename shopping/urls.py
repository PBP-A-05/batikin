from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.filter_products, name='filter_products'),
    path('<uuid:pk>/', views.product_detail, name='product_detail'),
    path('<uuid:pk>/check/', views.product_detail_check, name='product_detail_check'),
    path('add/<uuid:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
]