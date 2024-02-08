from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
  
  path('place_order', views.place_order, name='place_order'),
  path('order_history/', views.Order_history, name='order_history'),


  ]