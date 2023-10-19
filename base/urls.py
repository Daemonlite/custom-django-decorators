from django.urls import path
from base import views

urlpatterns = [
    path('', views.get_tasks),
    path('create/', views.create_task),
]