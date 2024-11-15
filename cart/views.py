from http.client import responses

from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart #Cart Session
from store.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart_summary.html", {"cart_products":cart_products})

def cart_add(request):
    # Get the cart
    cart = Cart(request)

    #Test for Post
    if request.POST.get('action') == 'post': #Lower case post is mentioned in the Ajax action

        #Get stuff from AJAX
        product_id = int(request.POST.get('product_id'))

        #Search product in DB
        product = get_object_or_404(Product, id=product_id)

        #Save to session
        cart.add(product=product) #Whole model object will be added

        #Get cart quantity
        cart_quantity = cart.__len__()

        #Return JSON response
        #response = JsonResponse({"Product Name ": product.name}) #Will reference Product Model name
        response = JsonResponse({"qty": cart_quantity})
        return response

def cart_delete(request):
    pass

def cart_update(request):
    pass
