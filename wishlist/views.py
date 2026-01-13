from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product


class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")

        product = Product.objects.get(id=product_id)

        WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)



class WishlistItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        wishlist = Wishlist.objects.get(user=request.user)
        item = WishlistItem.objects.get(
            wishlist=wishlist, product_id=product_id
        )
        item.delete()

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

# Create your views here.
