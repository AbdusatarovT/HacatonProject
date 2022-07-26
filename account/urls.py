from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from account.views import RegisterApiView, ActivationView, UserLoginView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterApiView.as_view()),
    path('active/<uuid:activation_code>/', ActivationView.as_view()),
    path('login/', UserLoginView.as_view()),
]