from django.urls import path
from . import views 

app_name = 'comment_review' 

urlpatterns = [
    path('create/', views.create_review, name='create_review'),
]
