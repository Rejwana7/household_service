from django.contrib import admin
from django.urls import path,include
from .import views
from .views import ViewCartView
urlpatterns = [
  
  path('service/<int:id>/', views.service_detail, name='service_detail'),
  path('submit_review/<int:id>/',views.Submit_review, name='submit_review'),
  path('update_review/<int:id>/',views.Update_review, name='update_review'),
  path('add_to_cart/<int:service_id>/',views.Add_to_Cart, name='add_to_cart'),
  # path('view_cart/',views.View_Cart, name='view_cart'),
  path('view_cart/',ViewCartView.as_view(), name='view_cart'),
  # path('pluscart/',views.plus_cart),
  path('increase_quantity/<int:cart_id>',views.increase_quantity,name='increase_quantity'),
  path('decrease_quantity/<int:cart_id>',views.decrease_quantity,name='decrease_quantity'),
  path('remove_cart/<int:cart_id>',views.remove_cart,name='remove_cart'),
  
  # path('category_detail/<slug:category_slug>/',views.category_detail_view,name='category_detail'),
  # path('category_list/',views.categories_list,name='category_list'),
  # path('categories/<slug:category_slug>/', views.categories_list, name='categories_list'),
  # path('category/<int:id>/', views.category_detail, name='category_detail'),
  path('all-services/', views.all_services, name='all_services'),
  path('category/<slug:category_slug>/', views.services_by_category, name='services_by_category'),
 ]










