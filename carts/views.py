from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id is required"},
                status=400
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=404
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )

        if not created:
            item.quantity += 1
            item.save()

        return Response(CartSerializer(cart).data)


class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id):
        quantity = request.data.get("quantity")

        if quantity is None or quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1"},
                status=400
            )

        try:
            item = CartItem.objects.get(
                cart__user=request.user,
                product_id=product_id
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found in cart"},
                status=404
            )

        item.quantity = quantity
        item.save()

        return Response(CartSerializer(item.cart).data)

    def delete(self, request, product_id):
        try:
            item = CartItem.objects.get(
                cart__user=request.user,
                product_id=product_id
            )
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Item not found"},
                status=404
            )

        item.delete()
        cart = Cart.objects.get(user=request.user)
        return Response(CartSerializer(cart).data)
