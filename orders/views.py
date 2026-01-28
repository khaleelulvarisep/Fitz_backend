import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from carts.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer
from products.models import Product
from products.models import Product
from carts.models import Cart, CartItem
from razorpay.errors import SignatureVerificationError


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)




class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        product_id = data.get("product_id")  # 👈 Buy Now check

        order_items = []
        total = 0

        # ================= BUY NOW =================
        if product_id:
            product = Product.objects.get(id=product_id)
            quantity = int(data.get("quantity", 1))

            total = product.price * quantity

            order_items.append({
                "product": product,
                "quantity": quantity,
                "price": product.price,
            })

        # ================= CART CHECKOUT =================
        else:
            cart = Cart.objects.get(user=request.user)

            if not cart.items.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            for item in cart.items.all():
                total += item.product.price * item.quantity
                order_items.append({
                    "product": item.product,
                    "quantity": item.quantity,
                    "price": item.product.price,
                })

        # ================= ORDER DATA =================
        order_data = {
            "user": request.user,
            "full_name": data["full_name"],
            "phone": data["phone"],
            "address": data["address"],
            "city": data["city"],
            "state": data["state"],
            "pincode": data["pincode"],
            "payment_method": data["payment_method"],
            "total_amount": total,
        }

        # ================= CASH ON DELIVERY =================
        if data["payment_method"] == "COD":
            order = Order.objects.create(**order_data)

            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"],
                )

            # Clear cart only for cart checkout
            if not product_id:
                cart.items.all().delete()

            return Response({"message": "Order placed successfully"},status=status.HTTP_200_OK)

        # ================= ONLINE PAYMENT =================
        razorpay_order = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": 1,
        })

        order = Order.objects.create(
            **order_data,
            razorpay_order_id=razorpay_order["id"],
            buy_now_product=product if product_id else None,
            buy_now_quantity=quantity if product_id else None,
        )

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "amount": total,
            "key": settings.RAZORPAY_KEY_ID,
            "order_id": order.id,
        })



class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })
        except SignatureVerificationError:
            return Response({"error": "Invalid payment signature"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.get(razorpay_order_id=data["razorpay_order_id"])
        order.payment_status = "PAID"
        order.razorpay_payment_id = data["razorpay_payment_id"]
        order.save()

        #  BUY NOW CASE
        if order.buy_now_product:
            OrderItem.objects.create(
                order=order,
                product=order.buy_now_product,
                quantity=order.buy_now_quantity,
                price=order.buy_now_product.price,
            )

        #  CART CHECKOUT CASE
        else:
            cart = Cart.objects.get(user=request.user)
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
            cart.items.all().delete()

        return Response({"message": "Payment successful"},status=status.HTTP_200_OK)

class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders,many=True,context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)
        serializer = OrderSerializer( order, context={"request": request})
        return Response(serializer.data,status=status.HTTP_200_OK)




client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class BuyNowOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))

        product = Product.objects.get(id=product_id)

        total = product.price * quantity

        order_data = {
            "user": request.user,
            "full_name": data["full_name"],
            "phone": data["phone"],
            "address": data["address"],
            "city": data["city"],
            "state": data["state"],
            "pincode": data["pincode"],
            "payment_method": data["payment_method"],
            "total_amount": total,
        }

        # ✅ CASH ON DELIVERY
        if data["payment_method"] == "COD":
            order = Order.objects.create(**order_data)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            return Response({
                "message": "Order placed successfully.",
                "order_id": order.id
            },status=status.HTTP_200_OK)

        #  ONLINE          PAYMENT (RAZORPAY)
        razorpay_order = client.order.create({
            "amount": int(total * 100),  # paise
            "currency": "INR",
            "payment_capture": 1,
        })

        order = Order.objects.create(
            **order_data,
            razorpay_order_id=razorpay_order["id"],
        )

        return Response({
            "razorpay_order_id": razorpay_order["id"],
            "amount": total,
            "key": settings.RAZORPAY_KEY_ID,
            "order_id": order.id
        },status=status.HTTP_200_OK)
