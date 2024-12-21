from django.urls import path
from . import views
from uuid import UUID

app_name = 'comment_review'

urlpatterns = [
    path('review/<uuid:product_id>/', views.create_review, name='create_review'),
    path('edit/<uuid:review_id>/<uuid:product_id>/', views.edit_review, name='edit_review'),
    path('reviews/delete/<uuid:review_id>/', views.delete_review, name='delete_review'),
    path('json/', views.show_json, name='show_json'),
    path('json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('get-reviews/<uuid:product_id>/', views.get_product_reviews, name='get_product_reviews'),
    path('review/json/<uuid:id>/', views.show_json_by_id, name='show_json_by_id'),
    path('review/create/', views.create_review_flutter, name='create_review_flutter'),
]