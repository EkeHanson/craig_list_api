# from django.shortcuts import render
# from django.shortcuts import redirect
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
# from django.contrib.auth import authenticate, login
# from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializer import CustomUserSerializer
from .models import CustomUser


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



