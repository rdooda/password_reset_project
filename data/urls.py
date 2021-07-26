from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/index/', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('forget/', views.forget_password, name='forget_password'),
    path('change_password/<token>/', views.change_password, name='change_password'),
]
