from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("centre/register", views.add_centre, name="add_centre"),
    path("logout", views.logout_view, name="logout"),

    path("", views.index, name="index"),
    path("centre/account", views.account_centre, name="account_centre"),

    path("api/centres", views.get_centres, name="centres"),
    path("api/edit/username", views.edit_username, name="edit_username"),
    path("api/edit/password", views.edit_password, name="edit_password")
]
