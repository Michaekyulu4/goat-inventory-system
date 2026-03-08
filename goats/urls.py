from django.urls import path
from . import views

urlpatterns = [
    path('', views.goat_list, name='goat_list'),
    path('<int:pk>/', views.goat_detail, name='goat_detail'),
]