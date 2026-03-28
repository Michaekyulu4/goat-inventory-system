from django.urls import path
from . import views

urlpatterns = [
    path('', views.goat_list, name='goat_list'),
    path('add/', views.add_goat, name='add_goat'),
    path('<int:pk>/', views.goat_detail, name='goat_detail'),
    path('<int:pk>/death/', views.record_death, name='record_death'),
    path('<int:pk>/sale/', views.record_sale, name='record_sale'),
    path('', views.dashboard, name='dashboard'),
],