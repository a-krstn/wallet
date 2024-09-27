from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'wallet'

router = routers.DefaultRouter()

router.register(r'wallets', views.WalletViewSet, basename='wallet')
router.register(r'wallets/(?P<wallet_id>.+)/operation', views.OperationViewSet, basename='operation')

urlpatterns = [
    path('', include(router.urls))
]