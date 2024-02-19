
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status
from .serializer import CustomUserSerializer
from .models import CustomUser
from django.core.mail import send_mail
from django.http import JsonResponse
import secrets
import datetime



# class FacebookLoginView(CreateView):
#     model = CustomUser
#     fields = ["username", "email", "password"]
#     success_url = reverse_lazy("success_url_name")  # Change this with your own URL
#
#     def form_valid(self, form):
#         # Create the user object
#         user = form.save(commit=False)
#         # Set the password manually (otherwise it will be saved with an unhashed password)
#         user.set_password(form.cleaned_data.get("password"))
#         # Save the User object to the database
#         user.save()
#
#         # Get email and password
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#
#         # Authenticate the user with the unhashed password
#         authenticated_user = authenticate(email=email, password=password)
#
#         # Log in the user
#         login(self.request, authenticated_user)
#
#         return redirect(self.success_url)


class CreateUserAPIView(APIView):

    def get(self, request: Request):

        users = CustomUser.objects.all()
        if users:
            serializer = CustomUserSerializer(users, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        print("No user found")
        return Response(data='Errors', status=status.HTTP_404_NOT_FOUND)


    def post(self, request: Request):
        print(request.data)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def generate_reset_token():
    return secrets.token_urlsafe(16)


def send_reset_email(user):
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    user.save()
    send_mail(
        subject = 'Password Reset',
        message = 'Please click the following link to reset your password: http://127.0.0.1:9090/user/password/reset/confirm/?reset_token=' + reset_token,
        from_email = 'ekenehanson@gmail.com',  # Update with your email address
        recipient_list = [user.email],  # Send email to the user's email address
        fail_silently = False,
    )


class PasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(CustomUser, email=email)
        send_reset_email(user)
        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)

class PasswordResetConfirmAPIView(APIView):
    def post(self, request):
        reset_token = request.query_params.get('reset_token')
        password = request.data.get('password')  # Assuming password is provided in the request body

        # Retrieve the user based on the reset_token
        user = get_object_or_404(CustomUser, reset_token=reset_token)

        # Check if the reset token is expired
        if user.reset_token_expires < datetime.datetime.now():
            return Response({'error': 'Reset token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(password)
        user.reset_token = None
        user.reset_token_expires = None
        user.save()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)