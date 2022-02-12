from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.auth_login, name="login"),
    path("register", views.auth_register, name="register"),
    path("logout", views.auth_logout, name="logout"),
    path("passwords", views.passwords, name="passwords"),
    path("add-password", views.add_password, name="add-password"),
    path("check-password", views.check_password, name="check-password"),
    path("update-password", views.update_password, name="update-password"),
    path("delete-password/<password_id>", views.delete_password, name="delete-password")
]