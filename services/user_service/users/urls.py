from django.urls import path
from .import views


urlpatterns = [
    path("", views.AuthenticatedView.as_view()),
    path("login-or-register/", views.LoginOrRegisterView.as_view()),
    path("logout/", views.LogoutView.as_view()),
]