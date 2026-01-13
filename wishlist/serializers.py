from rest_framework import serializers
from .models import Wishlist,WishlistItem
class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    price = serializers.ReadOnlyField(source="product.price")
    image = serializers.ReadOnlyField(source="product.image")

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "product",
            "product_name",
            "price",
            "image",
        ]


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ["id", "items"]
