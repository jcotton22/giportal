from django.urls import  path

from accounts.views import (
    RegisterView,
    ActivateView,
    ChangePasswordView,
    PasswordResetView,
    PasswordResetConfirmView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name = "register"),
    path("activate/", ActivateView.as_view(), name = "activate"),
    path("login/", CustomTokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path("password/change/", ChangePasswordView.as_view(), name = "password_change"),
    path("password/reset/", PasswordResetView.as_view(), name = "password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name = "password_reset_confirm")
]