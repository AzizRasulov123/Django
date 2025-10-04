from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.show_login_page, name='login-page'),
    path('registration/', views.show_registration_page, name='registration-page'),
    path('logout/', views.logout_user, name='logout-user'),
    path('<str:username>/profile/', views.show_profile_page, name='profile')
]