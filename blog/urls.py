from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-homepage'),
    path('about/', views.about, name='blog-aboutpage'),
]