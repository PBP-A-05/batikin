from django.urls import path
from . import views 

app_name = 'comment_review' 

urlpatterns = [
    path('review/<uuid:product_id>/', views.create_review, name='create_review'),
    path('edit/<uuid:review_id>/<uuid:product_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<uuid:review_id>/', views.delete_review, name='delete_review'),
]