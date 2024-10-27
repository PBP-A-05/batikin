from django.urls import path
from . import views 

app_name = 'comment_review' 

urlpatterns = [
    path('review/<int:product_id>/', views.create_review, name='create_review'),
    path('edit/<uuid:product_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
