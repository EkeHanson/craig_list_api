from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='products'),
    path('products/search/<str:search>/', views.search_product, name='products-search'),
    path('products/search/category/<str:category>/', views.product_by_category, name='view-products-by-category'),
    path('cart/', views.CartItemListAPIView.as_view(), name='view-cart'),
    path('cart/add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove-from-cart/<int:cart_item_id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
]