from django.urls import path
from .views import UsersViewApi,UserBlockApi,ProductViewApi

urlpatterns = [
    path('users/',UsersViewApi.as_view()),
    path('users/<int:user_id>/block/',UserBlockApi.as_view()),
    path('products/',ProductViewApi.as_view()),
]
