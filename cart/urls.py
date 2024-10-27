from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),  
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),  # Update quantity of an item
    path('shopping/cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),  # Changed to uuid
    path('cart/remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),

]