from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    descp = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    descp = models.CharField(max_length=100)
    def __str__(self):
        return self.name