from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vote/<int:poll_id>/', views.vote, name='vote'),
    path('results/<int:poll_id>/', views.results, name='results'),
    path('create', views.create, name='create'),
]