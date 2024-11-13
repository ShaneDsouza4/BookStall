from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {"products": products})


def about(request):
        return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST': #Submitting form
        username = request.POST['username'] #On form name is username
        password = request.POST['password'] #On form name is password

        #Need to authenticate using django authenticate system
        user = authenticate(request, username=username, password=password)

        # If form is not empty, log them in
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('login')
    else: #They didn't fill the form, show webpage
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def register_user(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST) #Take all inputs from webpage, and put in signup form
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            #Login User
            user = authenticate(username=username, password=password)
            login(request, user) #here login occurs
            messages.success(request, 'Registration Success')
            return redirect('home')
        else:
            print("Form errors:", form.errors)
            messages.success(request, 'Registration Failed')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form}) #pass the form

def product(request, pk):
    productfetched = Product.objects.get(id=pk) #Gets specific product
    return render(request, 'product.html', {'product': productfetched})

def category(request, foo):
    foo = foo.replace('-', ' ') #replace - with spaces

    print(foo)
    #Fetch category from url
    try:
        #Search category
        categoryfetched = Category.objects.get(name=foo)

        #Get products with the category
        products = Product.objects.filter(category=categoryfetched)

        return render(request, 'category.html', {"products": products, 'category': categoryfetched} )
    except:
        messages.success(request, 'Category does not exist')
        return redirect('home')
