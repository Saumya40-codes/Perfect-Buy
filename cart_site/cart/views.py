from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Login, Products, Cart, Comments
from .forms import LoginForm, ProductsForm, CommentForm
from django.contrib.auth import authenticate, logout , login as login_dj
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Sum
# Create your views here.


def index(request):
    return render(request, 'cart/home.html')

def login(request):
    name = 'login'
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        try:
            username = User.objects.get(username=user)
        except:
            form = LoginForm()
            context = {'form': form, 'name': name}
            messages.error(request, 'User not found')
            return render(request, 'cart/login.html', context)
        
        username_auth = authenticate(request, username=username, password=password)
        if username_auth is not None:
            login_dj(request, username_auth)
            return redirect('publish')
        else:
            form = LoginForm()
            context = {'form': form, 'name': name}
            messages.error(request, 'Password is incorrect')
            return render(request, 'cart/login.html', context)
    form = LoginForm()
    context = {'form': form, 'name': name}
    return render(request, 'cart/login.html', context)

def signup(request):
    name = 'signup'
    if request.method == 'POST':
        frm = UserCreationForm(request.POST)
        name = request.POST.get('username')
        if frm.is_valid():
            user = frm.save(commit=False)
            user.username = user.username.lower()
            user.save()
            context = {'name': name}
            login_dj(request, user)
            return render(request, 'cart/publish.html', context)
        else:
            messages.error(request, 'Error creating account as username already exists')
            return render(request, 'cart/login.html')
    form_s = UserCreationForm()
    context = {'form_s': form_s, 'name': name}
    return render(request, 'cart/login.html', context)

@login_required(login_url='login')
def publish(request):
    if request.method == 'POST':
        name = request.POST.get('q') if request.POST.get('q') != None else ''
        items = Products.objects.filter(
            Q(name__icontains=name) | 
            Q(descp__icontains=name)
        )
        item_count = items.count()
        context = {'items': items, 'item_count': item_count}
        return render(request, 'cart/publish.html', context)
    items = Products.objects.all()
    context = {'items': items}
    return render(request, 'cart/publish.html', context)

@login_required(login_url='login')
def publish_prod(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product published successfully')
            return redirect('publish_prod')
    form = ProductsForm()
    context = {'form': form}
    return render(request, 'cart/publish_prod.html', context)

def view(request, pk):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_price = request.POST.get('item_price')
        item_descp = request.POST.get('item_descp')
        name = User.objects.get(username=request.user)
        cart_item, created = Cart.objects.get_or_create(
            user=name,
            name=item_name,
            price=item_price,
            descp=item_descp,     
        )
        if created:
           cart_item.save()
        messages.success(request, 'Item added to cart successfully')
        pk = int(request.POST.get('item_id'))
        item = Products.objects.get(id=pk)
        form = CommentForm()
        context = {'item': item, 'form': form}
        return render(request, 'cart/view.html', context)
    item = Products.objects.get(id=pk)
    form = CommentForm()
    context = {'item': item, 'form': form}
    return render(request, 'cart/view.html', context)

def cart(request):
    name = User.objects.get(username=request.user)
    items = Cart.objects.filter(user=name)
    item_count = items.count()
    total_price = items.aggregate(Sum('price'))['price__sum'] or 0
    context = {'items': items, 'item_count': item_count, 'total_price': total_price}
    return render(request, 'cart/cart_items.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')

def comment(request):
    if request.method == 'POST':
        pk = request.POST.get('item_ids')
        com = CommentForm(request.POST)
        if com.is_valid():
            com.save()
        item = Products.objects.get(id=pk)
        form = CommentForm()    
        comments = Comments.objects.all()
        context = {'comment': comments, 'item': item,'form': form}
        return render(request, 'cart/view.html', context)
    
def delete(request, pk):
    item = Cart.objects.get(id=pk)
    item.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect('cart')
