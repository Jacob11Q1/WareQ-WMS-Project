from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("users/", views.user_list, name="user_list"),  # admin only
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),  # admin only
]
