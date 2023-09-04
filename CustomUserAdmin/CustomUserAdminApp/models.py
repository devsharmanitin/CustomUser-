from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.





class CustomUser(AbstractUser):
    username = models.CharField(max_length=244,unique=True,null=True , blank=True)
    email = models.EmailField(('email_address'),unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    