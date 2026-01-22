from django.shortcuts import render
from rest_framework.views import APIView
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UserBlockSerializer,ProductSerializer,OrderStatusUpdateSerializer
from orders.serializers import OrderSerializer
from products.models import Product
from orders.models import Order
from rest_framework.permissions import IsAdminUser

    #////////////////User//////////////////////////////

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

#///////////////////Products///////////////////////////////

class ProductListCreateApiView(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetailAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

#/////////////////////////Orders////////////////////////////////



# class OrderListApiView(APIView):
#     def get(self,request):
#         orders=Order.objects.all()
#         serializer=OrderSerializer(orders,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
class OrderListApiView(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderStatusUpdateApiView(APIView):
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderStatusUpdateSerializer(
            order,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Order status updated successfully",
                    "status": serializer.data["status"]
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrderOfSpecificUserApiView(APIView):
    def get(self,request,pk):
        orders=Order.objects.filter(user_id=pk)
        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
# Create your views here.