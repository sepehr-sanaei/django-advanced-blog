from django.urls import path, include
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='auth-token'),
    # change password
    path('change-password/', views.ChangePasswordVIew.as_view(), name='change-password'),
    # reset password
    # logout
    path('api-token-logout/', views.CustomDiscardToken.as_view(), name='logout-auth-token'),
    # login
    path('jwt/create/', TokenObtainPairView.as_view(), name="jwt-create"),
    path('jwt/refresh/', TokenRefreshView.as_view(), name="jwt-refresh"),
    path('jwt/verify/', TokenVerifyView.as_view(), name="jwt-verify"),
    # profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),

]