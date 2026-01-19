from rest_framework import serializers
from accounts.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['is_active']