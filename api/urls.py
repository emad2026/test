from django.urls import path
from accounts.views import (
    ClientLoginView, ClientLogoutView, ClientPasswordResetRequestView, ClientRegisterView,
    ClientResendOTPView, ClientResetPasswordView,clientChangePasswordView,
    CaptainLoginView, CaptainLogoutView, CaptainPasswordResetRequestView, CaptainRegisterView,
    CaptainResendOTPView, CaptainResetPasswordView,CaptainChangePasswordView, VerifyEmailView
)
from rest_framework_simplejwt.views import TokenRefreshView # type: ignore
from  accounts.views import ClientUpdateView, ClientProfileUpdateView

urlpatterns = [
    # Resend OTP
    path('resend-otp/captain/', CaptainResendOTPView.as_view(), name='captain-resend-otp'),
    path('resend-otp/client/', ClientResendOTPView.as_view(), name='client-resend-otp'),

    # Login, logout, and token refresh
    path('login/captain/', CaptainLoginView.as_view(), name='captain-login'),
    path('login/client/', ClientLoginView.as_view(), name='client-login'),
    path('logout/captain/', CaptainLogoutView.as_view(), name='captain-logout'),
    path('logout/client/', ClientLogoutView.as_view(), name='client-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Reset password
    path('reset-password/captain/', CaptainPasswordResetRequestView.as_view(), name='captain-reset-password-request'),
    path('confirm-reset-password/captain/', CaptainResetPasswordView.as_view(), name='captain-reset-password-confirm'),
    path('reset-password/client/', ClientPasswordResetRequestView.as_view(), name='client-reset-password-request'),
    path('confirm-reset-password/client/', ClientResetPasswordView.as_view(), name='client-reset-password-confirm'),

    # Change password
    path('change-password/captain/',CaptainChangePasswordView.as_view(), name='captain-change-password'),
    path('change-password/client/',clientChangePasswordView.as_view(), name='client-change-password'),

   #registration
    path('register/captain/', CaptainRegisterView.as_view(), name='register-captain'),
    path('register/client/', ClientRegisterView.as_view(), name='register-client'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    #profile 
    path('client/update/', ClientUpdateView.as_view(), name='client-update'),
    path('client/profile/update/', ClientProfileUpdateView.as_view(), name='client-profile-update'),

]