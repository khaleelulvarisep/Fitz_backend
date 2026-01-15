import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from carts.models import Cart
from .models import Order, OrderItem


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_method = request.data.get("payment_method")
        cart = Cart.objects.get(user=request.user)

        total = sum(
            item.product.price * item.quantity for item in cart.items.all()
        )

        # 👉 CASH ON DELIVERY
        if payment_method == "COD":
            order = Order.objects.create(
                user=request.user,
                payment_method="COD",
                payment_status="PENDING",
                total_amount=total,
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            cart.items.all().delete()

            return Response({"message": "Order placed with COD"})

        # 👉 ONLINE PAYMENT (RAZORPAY)
        razorpay_order = client.order.create(
            {
                "amount": int(total * 100),
                "currency": "INR",
                "payment_capture": 1,
            }
        )

        order = Order.objects.create(
            user=request.user,
            payment_method="ONLINE",
            payment_status="PENDING",
            total_amount=total,
            razorpay_order_id=razorpay_order["id"],
        )

        return Response(
            {
                "order_id": order.id,
                "razorpay_order_id": razorpay_order["id"],
                "amount": total,
                "key": settings.RAZORPAY_KEY_ID,
            }
        )


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            }
        )

        order = Order.objects.get(razorpay_order_id=data["razorpay_order_id"])
        order.payment_status = "PAID"
        order.razorpay_payment_id = data["razorpay_payment_id"]
        order.save()

        cart = Cart.objects.get(user=request.user)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        cart.items.all().delete()

        return Response({"message": "Payment successful"})
