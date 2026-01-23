from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductListView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        # Get query params
        search = request.GET.get("search", "")
        category = request.GET.get("category", "all")

        # Apply filters
        if search:
            queryset = queryset.filter(name__icontains=search)

        if category and category != "all":
            queryset = queryset.filter(category=category)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# Create your views here.
