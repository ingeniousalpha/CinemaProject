"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import re_path
from firstapp import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r"^bal", views.hello),
    re_path(r"^about", views.about),
    path("products/<int:pr_id>/", views.products),
    path("products/", views.products),
    re_path(r"^users/", views.users),
    path("contacts/", views.contacts),
    path("details/", views.details),
    path("logup/", views.logup),
    path("login/", views.login),
    path("profile/", views.profile),
    path("history/", views.history),
    path("cinemas/", views.cinemas),
    path("logout/", views.logout),
    path("films/<str:cin>/", views.films),
    path("myfilm/", views.myfilm),
    path("booking/", views.booking),
    path("bookseats/", views.bookseats),
]




