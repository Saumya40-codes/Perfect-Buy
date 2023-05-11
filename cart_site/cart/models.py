from django.db import models

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