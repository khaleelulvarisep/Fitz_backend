# orders/urls.py
from django.urls import path
from .views import CreateOrderView, VerifyPaymentView,OrderDetailView,MyOrdersView,BuyNowOrderView

urlpatterns = [
    path("", MyOrdersView.as_view()),               # /api/orders/
    path("<int:order_id>/", OrderDetailView.as_view()),
    path("create/", CreateOrderView.as_view()),
    path("verify/", VerifyPaymentView.as_view()),
    path("buy-now/", BuyNowOrderView.as_view()),
]
