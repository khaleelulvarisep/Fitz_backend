from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UserBlockSerializer,ProductSerializer
from products.models import Product


class UsersViewApi(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class UserBlockApi(APIView):
    def patch(self,request,user_id):
        user=User.objects.get(id=user_id)
        serializer=UserBlockSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "User status updated successfully",
                "is_active": user.is_active
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)



class ProductViewApi(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# Create your views here.