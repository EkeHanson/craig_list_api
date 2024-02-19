# from django.shortcuts import render
#
# from rest_framework import viewsets
# from rest_framework import filters
# from .models import Product, Cart, CartItem, Order
# from .serializer import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer
#
#
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name', 'description', 'category', 'price', 'location']
#     ordering_fields = ['name', 'price', 'category', 'brand', 'location', ]
#
#
# class CartViewSet(viewsets.ModelViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#
#
# class CartItemViewSet(viewsets.ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#
#
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
from django.core import paginator
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Q
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Product, Cart, CartItem, Order
from .serializer import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer


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


# class CartItemListAPIView(APIView):
#     def get(self, request):
#         cart_items = CartItem.objects.all()
#         serializer = CartItemSerializer(cart_items, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddToCartView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        return Response({"message": "Item added to your cart"}, status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    def delete(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from your cart"}, status=status.HTTP_204_NO_CONTENT)


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


# @api_view(http_method_names=['GET'])
# def search_product(request: Request):
#     # query = request.GET.get('q', '')
#     # if query:
#     #     products = Product.objects.filter(models.Q(header__icontains=query))
#     # else:
#     #     products = Product.objects.all()
#     # serializer = ProductSerializer(products, many=True)
#     # return Response(serializer.data, status=status.HTTP_200_OK)
#     search = request.query_params.get('name')
#     if search:
#         products = Product.objects.filter(name__icontains=search)
#     else:
#         products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

@api_view(http_method_names=['GET'])
def search_product(request: Request):
    search = request.query_params.get('search')
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