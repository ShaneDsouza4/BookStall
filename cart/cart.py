from django.contrib.sites import requests

from store.models import Product


class Cart():
    def __init__(self, request): # initialize class, Req is user request
        self.session = request.session

        #Fetch current session key if exists
        cart = self.session.get('session_key')

        # If user is new, no session key and will be created
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure shopping cart is available on all pages, and keep track
        self.cart = cart

    #Add functionality
    def add(self, product):
        product_id = str(product.id)

        #Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)} #Will be added in session when decoded

        self.session.modified = True

    #Filter the length
    def __len__(self):
        return len(self.cart)

    #Get cart details
    def get_prods(self):

        #Get ids from cart
        product_ids = self.cart.keys() #Keys because product id is getting added to cart via the add functiona above. Set up as dictionary

        # Search and return products in DB via ids and Product model
        products = Product.objects.filter(id__in=product_ids)
        return products



