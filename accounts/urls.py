from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign-up/', UserSignUpView.as_view(), name='user_sign_up'),
    path('verify-otp/', UserOTPVerifyView.as_view(), name='verify_otp'),
]