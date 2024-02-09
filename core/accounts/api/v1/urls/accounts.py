from django.urls import path, include
from .. import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # registration
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    path(
        "api-token-auth/", views.CustomAuthToken.as_view(), name="auth-token"
    ),
    # test
    path("test/", views.TestEmail.as_view(), name="test"),
    # activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiToken.as_view(),
        name="account-activation",
    ),
    path(
        "activation/confirm-resend/",
        views.ActivationResendApiToken.as_view(),
        name="activation-resend",
    ),
    # change password
    path(
        "change-password/",
        views.ChangePasswordVIew.as_view(),
        name="change-password",
    ),
    # reset password
    # path("reset-password/", views.ResetPasswordApiView.as_view(), name="reset-password"),
    # logout
    path(
        "api-token-logout/",
        views.CustomDiscardToken.as_view(),
        name="logout-auth-token",
    ),
    # login
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
