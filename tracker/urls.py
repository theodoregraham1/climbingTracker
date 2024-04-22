from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("centre/register", views.add_centre, name="add_centre"),

    path("", views.index, name="index"),
]
