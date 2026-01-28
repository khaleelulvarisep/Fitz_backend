from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .views import RegisterAPIView,UserMeView,CustomTokenObtainPairView,GoogleAuthAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserMeView.as_view()),
    path("google/", GoogleAuthAPIView.as_view()),

]
