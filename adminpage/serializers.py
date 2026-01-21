from rest_framework import serializers
from accounts.models import User
from products.models import Product
from orders.models import Order
      #/////////////////User///////////////////////

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['is_active']

    #////////////////////Products///////////////////////////

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

#///////////////////////Orders//////////////////////////////
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'