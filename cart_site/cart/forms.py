from django.forms import ModelForm

from .models import Login, Products, Comments


class LoginForm(ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password']

class ProductsForm(ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'descp']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['title', 'comment']