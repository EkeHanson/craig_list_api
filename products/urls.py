from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='products'),
    path('products/search/', views.search_product, name='products-search'),
    path('cart', views.CartListAPIView.as_view(), name='view-cart'),
    path('cart/add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove-from-cart/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
]
