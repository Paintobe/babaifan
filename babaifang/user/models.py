from django.db import models

# Create your models here.

class Users(models.Model):
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=50,default='')