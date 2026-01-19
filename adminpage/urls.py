from django.urls import path
from .views import UsersViewApi

urlpatterns = [
    path('users/',UsersViewApi.as_view()),
]
