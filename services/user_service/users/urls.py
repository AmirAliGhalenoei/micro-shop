from django.urls import path
from .import views


urlpatterns = [
    path("", views.AuthenticatedView.as_view()),
    path("login-or-register/", views.LoginOrRegisterView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("profile/", views.UserProfileView.as_view()),
    path("profile/edit-info/", views.EditInformationView.as_view()),
    path("profile/set-email/", views.SetEmailView.as_view()),
    path("profile/email-verify/", views.EmailVerifyView.as_view()),
    path("profile/set-password/", views.SetPasswordAcountView.as_view())
]