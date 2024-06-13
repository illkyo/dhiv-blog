from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='blog-homepage'),
    # path('about/', views.about, name='blog-aboutpage'),
    path('', views.Home.as_view(), name='blog-homepage'),
    path('about/', views.About.as_view(), name='blog-aboutpage'),
    path('profile/', views.Profile.as_view(), name='blog-profilepage'),
]