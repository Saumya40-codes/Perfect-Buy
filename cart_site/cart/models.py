from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Products(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    prod_img = models.ImageField(upload_to='images/')
    price = models.IntegerField()
    descp = models.CharField(max_length=400)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    img = models.ImageField( upload_to='images/')
    price = models.IntegerField()
    descp = models.CharField(max_length=400)
    def __str__(self):
        return self.name
    
class Comments(models.Model):
    name = models.ForeignKey(Products, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=50)
    comment = models.CharField(max_length=500)
    def __str__(self):
        return self.title