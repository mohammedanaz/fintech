from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('advisor', 'Financial Advisor')
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='individual')
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
