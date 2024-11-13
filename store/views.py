from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
