from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("company/settings/", views.company_settings, name="company_settings"),
    path("company/invite/", views.invite_user, name="invite_user"),
    path("users/", views.user_list, name="user_list"),
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),
    path("billing/", views.billing_dashboard, name="billing"),

]
