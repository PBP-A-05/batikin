from django.urls import path
from . import views
from .views import workshop_detail, workshop_product_list, workshop_list

urlpatterns = [
    path('workshop-products/', workshop_product_list, name='workshop_product_list'),
    path('workshop/<int:pk>/', workshop_detail, name='workshop_detail'),
    path('workshops/', workshop_list, name='workshop_list'),
]
