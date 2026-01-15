# orders/urls.py
from django.urls import path
from .views import CreateOrderView, VerifyPaymentView

urlpatterns = [
    path("create/", CreateOrderView.as_view()),
    path("verify/", VerifyPaymentView.as_view()),
]
