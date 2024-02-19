from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from datetime import date


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, date_of_birth, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, user_type, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff set to True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser set to True")

        return self.create_user(email=email, password=password, user_type=user_type, **extra_fields)


class CustomUser(AbstractBaseUser):
    #fields to store the password reset token and its expiration time in your CustomUser model.
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(max_length=255)  # Specify a maximum length for the bio
    email = models.EmailField(max_length=80, unique=True)
    date_of_birth = models.DateField(null=False)  # Ensure date_of_birth is not null
    user_type = models.CharField(max_length=10, choices=[('owner', 'Owner'), ('admin', 'Admin'), ('client', 'Client')])

    def calculate_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email
    
