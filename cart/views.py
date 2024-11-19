from http.client import responses

from django.shortcuts import render, get_object_or_404, redirect

from store.views import product
from .cart import Cart #Cart Session
from store.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    #Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods

    quantities = cart.get_quants

    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities})

def cart_add(request):
    # Get the cart
    cart = Cart(request)

    #Test for Post
    if request.POST.get('action') == 'post': #Lower case post is mentioned in the Ajax action

        #Get stuff from AJAX
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #Search product in DB
        product = get_object_or_404(Product, id=product_id)

        #Save to session
        cart.add(product=product, quantity=product_qty) #Whole model object will be added

        #Get cart quantity
        cart_quantity = cart.__len__()

        #Return JSON response
        #response = JsonResponse({"Product Name ": product.name}) #Will reference Product Model name
        response = JsonResponse({"qty": cart_quantity})
        return response

def cart_delete(request):
    # Instance of cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':  # Lower case post is mentioned in the Ajax action
        # Get stuff from AJAX
        product_id = int(request.POST.get('product_id'))

        # Fetch the Product instance
        product = get_object_or_404(Product, id=product_id)

        # Update cart
        cart.delete(product=product)

        # Return Response
        response = JsonResponse({"success":"Product Deleted"})  # Passing qty to get response
        return response

def cart_update(request):
    #Instance of cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':  # Lower case post is mentioned in the Ajax action
        # Get stuff from AJAX
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # Fetch the Product instance
        product = get_object_or_404(Product, id=product_id)

        #Update cart
        cart.update(product=product, quantity=product_qty)

        #Return Response
        response = JsonResponse({"qty": product_qty}) #Passing qty to get response
        return response

