from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import OrderView

router = DefaultRouter()
router.register('', OrderView)

urlpatterns = [
    path('', include(router.urls))
]

