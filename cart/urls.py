from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),  
    path('sort/', views.sort_cart_items, name='sort_cart_items'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('shopping/cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),  # Changed to uuid
    path('cart/remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('api/get-order/', views.get_orders_by_user, name='get-order'),
    
    # flutter
    path('api/view/', views.view_cart_json, name='view_cart_json'),
    path('api/update/<int:item_id>/', views.update_cart_item_json, name='update_cart_item_json'),
    path('api/remove/<int:item_id>/', views.remove_from_cart_json, name='remove_from_cart_json'),
    path('api/sort/', views.sort_cart_items_json, name='sort_cart_items_json'),
]