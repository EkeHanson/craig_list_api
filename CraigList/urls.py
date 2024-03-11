from django.contrib import admin
from django.urls import path, include
from django.urls import re_path

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenVerifyView,
    TokenRefreshView,
)

from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title="Port Harcourt Craig List API",
      default_version='v1',
      description="This is a backend API to be integrated into a Javascript frontend Application to List Products and Shop",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ekenehanson@gmail.com"),
      license=openapi.License(name="Copyright 2024"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Dummy views for the purpose of adding tags
def user_view(request):
    pass

def products_view(request):
    pass


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(('user_registration.urls', 'user'), namespace='User')),  # Group under 'User' tag
    path('', include(('products.urls', 'products'), namespace='Products')),          # Group under 'Products' tag

    # swagger ui
      # swagger ui
    path('<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # used to get tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


