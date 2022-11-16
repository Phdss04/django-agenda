from django.urls import path
from . import views
from contatos.views import index

urlpatterns = [
     path("", index),
     path("login/", views.login, name='login'),
     path("logout/", views.logout, name='logout'),
     path("register/", views.register, name='register'),
]

