from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Q
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Product, Cart, CartItem, Order
from user_registration.permissions import IsClient
from .serializer import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer
import paypalrestsdk
from django.urls import reverse
from user_registration.models import CustomUser


class ProductListAPIView(APIView):
    def get(self, request: Request):

        products = Product.objects.all()
        # Create a Paginator object with 5 items per page
        paginator = Paginator(products, 15)

        # Get the requested page number
        page_number = request.GET.get('page')

        # Get the Page object for the requested page number
        page_obj = paginator.get_page(page_number)

        # Serialize the Page object
        serializer = ProductSerializer(page_obj, many=True)

        response_data = {
            'list of records': serializer.data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'total_pages': paginator.num_pages,
            'current_page_number': page_obj.number,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartListAPIView(APIView):
    def get(self, request: Request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCartItemListAPIView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1

        total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

        # Apply the discount if a promo code is set
        if cart.promo_code:
            discount = cart.promo_code.discount.amount
            total_price *= (1 - discount / 100)

        cart_item.save()
        return Response({"message": "Item added to your cart", "total_price": total_price}, status=status.HTTP_200_OK)


class UserRemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from your cart"}, status=status.HTTP_204_NO_CONTENT)


class AddToCartView(APIView):
    def post(self, request, product_id, format=None):
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart

        # Calculate the total price
        total_price = sum(Product.objects.get(id=id).price * quantity for id, quantity in cart.items())

        return Response({"message": "Item added to your cart", "total_price": total_price}, status=status.HTTP_200_OK)


class CartDetailView(APIView):
    def get(self, request, format=None):
        cart = request.session.get('cart', {})
        cart_items = Product.objects.filter(id__in=cart.keys())
        for item in cart_items:
            item.quantity = cart[str(item.id)]

        # Calculate the total price
        total_price = sum(item.price * item.quantity for item in cart_items)

        return Response({"cart_items": [{"product_id": item.id, "quantity": item.quantity} for item in cart_items], "total_price": total_price}, status=status.HTTP_200_OK)


class OrderList(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
def search_product(request: Request, search):
    search = request.query_params.get(search, '')
    if search:
        products = Product.objects.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search) |
            Q(location__icontains=search) |
            Q(category__icontains=search)
            # Add more fields as needed
        )
    else:
        products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['GET'])
def product_by_category(request: Request, category):
    product = Product.objects.filter(category=category)
    if product:
        serializer = ProductSerializer(product, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif category == 'all':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data='Error', status=status.HTTP_404_NOT_FOUND)


paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

class CreatePaymentView(APIView):
    def post(self, request):
        # Create Payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": '5.00',
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": str(total_price),
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        # Create Payment and return status
        if payment.create():
            for link in payment.links:
                if link.method == "REDIRECT":
                    redirect_url = str(link.href)
                    return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)


class ExecutePaymentView(APIView):
    def post(self, request):
        payment = paypalrestsdk.Payment.find(request.data['paymentID'])

        # Execute payment
        if payment.execute({"payer_id": request.data['payerID']}):
            return Response({"payment": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)


