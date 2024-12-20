from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.filter_products, name='filter_products'),
    path('<uuid:pk>/', views.product_detail, name='product_detail'),
    path('<uuid:pk>/check/', views.product_detail_check, name='product_detail_check'),
    path('wishlist/add/<uuid:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/get-product/<uuid:product_id>/', views.get_product, name='get_product'),
    path('json/', views.show_json, name='show_json'),
    path('json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'), 
    
    # flutter
    path('api/cart/add/<uuid:product_id>/', views.add_to_cart_json, name='add_to_cart_json'),
]