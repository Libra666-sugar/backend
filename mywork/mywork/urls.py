"""
URL configuration for mywork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.views.generic import TemplateView

from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("name/", views.show_name),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("register/", views.register),
    path("login/", views.user_login),
    path("create_post/", views.create_post),
    path("create_comment/", views.create_comment),
    path("delete_post/", views.delete_post),
    path("favorite_post/", views.favorite_post),
    path("show_posts/", views.show_posts),
    path("favorite/", views.show_favorited_posts),
    path("remove_favorite/", views.remove_favorite),
    path("user_center/", views.user_center),
    path("create_announcement/", views.create_announcement),
    path("show_announcements/", views.show_announcements),
    path("check_admin/", views.check_admin),
    path("show_articles/", views.show_articles)
]
