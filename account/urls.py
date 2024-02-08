from django.urls import path,include
from .views import UserRegistrationView,UserLoginView,UserProfileView,UpdateProfileView
from.import views
urlpatterns = [
   
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("login/",UserLoginView.as_view(),name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    # path('make_admin/<int:user_id>/',views.make_admin,name="make_admin"),
    path('make_admin/',views.make_admin,name="make_admin"),
    path('all_order_show/',views.all_order_show,name="all_order_show"),
    path('approve_order/<int:order_id>/',views.Approve_order,name="approve_order"),
    path('cancel_order/<int:order_id>/',views.Cancelled_order,name="cancel_order"),
    path('profile_view',UserProfileView.as_view(),name="profile_view"),
    path('profile_update/',UpdateProfileView.as_view(),name="profile_update"),
    path('edit_pass/',views.EditPasswordView.as_view(),name="edit_pass"),
    
]
   
    
