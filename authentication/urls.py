from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("verify_email/", views.VerifyEmailView.as_view(), name="verify_email"),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("user/", views.UserView.as_view()),
    path("refresh/", views.RefreshView.as_view()),
    path("reset_password/", views.RequestPasswordResetView.as_view()),
    path("confirm_password_reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="confirm_password_reset"),
    path("set_new_password/", views.SetNewPasswordView.as_view(),
         name="set_new_password")
]


