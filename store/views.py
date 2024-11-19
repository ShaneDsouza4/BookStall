from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm

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

def category_summary(request):
    # Fetch all categories
    categories = Category.objects.all()

    return render(request, 'category_summary.html', {"categories": categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)

        #If they are posting, or use their current instance
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        # THey filled the form
        if user_form.is_valid():
            user_form.save()

            #Log back in with updated details
            login(request, current_user)
            messages.success(request, 'Your account has been updated!')
            return redirect('home')

        #ELse they are going to the page to edit
        return render(request, 'update_user.html', {'user_form': user_form})
    else: #If user is not logged in
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')


def update_password(request):
    #User is logged in
    if request.user.is_authenticated:
        current_user = request.user

        #Did the fill out the form
        if request.method == 'POST':
            # User filled form and Posted
            form = ChangePasswordForm(current_user, request.POST)

            #Check if the form is valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated!')
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {"form":form})
    else: #Not logged in
        messages.success(request, 'You must be logged in to access this page')
        return redirect('home')
