from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.filter_products, name='filter_products'),  # Changed from api/products/
    path('<uuid:pk>/', views.product_detail, name='product_detail'),
    path('api/products/', views.filter_products, name='filter_products'),
]