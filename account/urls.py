from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from account.views import RegisterApiView, ActivationView, ChangePasswordView, ForgotPasswordView, ForgotPasswordComplete

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterApiView.as_view()),
    path('active/<uuid:activation_code>/', ActivationView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_completed/', ForgotPasswordComplete.as_view()),

]