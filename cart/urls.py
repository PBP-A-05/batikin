from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),  
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),  # Update quantity of an item
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from cart
    path('create_order/', views.create_order, name='create_order'),
    path('api/get-order/', views.get_orders_by_user, name='get-order'),
]