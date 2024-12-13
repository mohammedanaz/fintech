from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('sign-up/', UserSignUpView.as_view(), name='user_sign_up'),
    path('signup_verify-otp/', SignupOTPVerifyView.as_view(), name='signup_verify_otp'),
    path('sign-in/', SignInUserView.as_view(), name='sign_in'),
    path('login_verify-otp/', LoginOTPVerifyView.as_view(), name='login_verify_otp'),
]