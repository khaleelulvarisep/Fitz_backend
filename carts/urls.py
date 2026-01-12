from django.urls import path
from .views import CartView, CartItemUpdateView

urlpatterns = [
    path('', CartView.as_view()),
    path('item/<int:product_id>/', CartItemUpdateView.as_view()),
]
