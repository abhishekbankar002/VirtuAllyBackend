from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/uploadImage',views.getImage),
    path('api/register',views.registerUser),
    path('api/logIn',views.logIn),
    path('api/checkLogIn',views.checkLogin),
    path('api/tryImage',views.tryImage),
    path('api/getProducts', views.getProducts),
    path('api/get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),

]