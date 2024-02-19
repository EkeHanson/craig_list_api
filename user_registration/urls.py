from django.urls import path
from . import views

urlpatterns = [
    # path('login/facebook/', views.FacebookLoginView.as_view(), name='facebook_login'),
    path('create/', views.CreateUserAPIView.as_view(), name='create_user'),
    path('password/reset/', views.PasswordResetAPIView.as_view(), name='password_reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]
