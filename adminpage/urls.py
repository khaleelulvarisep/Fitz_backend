from django.urls import path
from .views import UsersViewApi,UserBlockApi,ProductListCreateApiView,ProductDetailAPIView,OrderListApiView,OrderStatusUpdateApiView

urlpatterns = [
    path('users/',UsersViewApi.as_view()),
    path('users/<int:user_id>/block/',UserBlockApi.as_view()),
    path('products/',ProductListCreateApiView.as_view()),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path('orders/',OrderListApiView.as_view()),
    path("orders/<int:order_id>/status/", OrderStatusUpdateApiView.as_view()),


]
