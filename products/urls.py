from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='products'),
    path('product/search/', views.search_product, name='products_search')
]
