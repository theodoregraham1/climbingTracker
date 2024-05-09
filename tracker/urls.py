from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("centre/register", views.add_centre, name="add_centre"),
    path("logout", views.logout_view, name="logout"),

    path("", views.index, name="index"),
    path("centres/<centre_id>", views.centre_page, name="centre_page"),

    path("account", views.account, name="account"),

    path("centre/walls/<id>", views.wall_settings, name="wall_settings"),
    path("centre/walls/add", views.add_wall, name="add_wall"),

    path("api/centres", views.get_centres, name="centres"),

    path("api/edit/username", views.edit_username, name="edit_username"),
    path("api/edit/password", views.edit_password, name="edit_password"),
    path("api/edit/image", views.edit_centre_image, name="edit_image"),
    path("api/edit/setters", views.edit_setters_list, name="edit_setters"),
    path("api/edit/<attribute>", views.edit_centre_attribute, name="edit_centre_attribute")
]
