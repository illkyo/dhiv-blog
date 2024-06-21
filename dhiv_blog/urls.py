"""
URL configuration for dhiv_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', blog_views.Home.as_view(), name='blog-homepage'),
    path('about/', blog_views.About.as_view(), name='blog-aboutpage'),
    path('login/', user_views.Login.as_view(), name='users-login'),
    path('profile/', user_views.Profile.as_view(), name='users-profilepage'),
    path('post/<int:pk>/', blog_views.PostDetail.as_view(), name='blog-postdetail'),
    path('post/new/', user_views.PostCreate.as_view(), name='blog-postcreate'),
    path('post/<int:pk>/update/', user_views.PostUpdate.as_view(), name='blog-postupdate'),
    # path('post/<int:pk>/delete/', user_views.PostDelete.as_view(), name='blog-postdelete')
    # path('register/', user_views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)