from rest_framework import serializers
from .models import Order, OrderItem


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = "__all__"


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "image",
            "quantity",
            "price",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.product.image  # THIS IS A STRING

        if not image:
            return None

        # If already full URL
        if image.startswith("http"):
            return image

        # If relative path
        if request:
            return request.build_absolute_uri(image)

        return image





class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["items"] = OrderItemSerializer(
            instance.items.all(),
            many=True,
            context=self.context
        ).data
        return data


