from .cart import Cart #Name of the Cart Class in cart.py

# Creating context processor so our cart can work on all pages
def cart(request):
    # Return default data from our cart
    return {'cart': Cart(request)} #From cart return the Cart Request