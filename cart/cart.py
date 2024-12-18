from itertools import product

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
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)} #Will be added in session when decoded
            self.cart[product_id] = int(product_qty)
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

    # Return cart for quantities
    def get_quants(self):
        quantitites = self.cart
        return quantitites

    #Product and qty and parameters sent in the view
    def update(self, product, quantity):

        #Add as string because of the dictionary {"3":4}
        product_id = str(product.id)
        product_qty = int(quantity)

        #Update session process
        # Get cart
        ourcart = self.cart

        #Update dictionary/cart
        #Find the key and change to the quantity we have
        ourcart[product_id] = product_qty

        # Modify the cart session
        self.session.modified = True

        # New updated cart
        thing = self.cart
        return thing

    def delete(self, product):
        #Get product ID
        product_id = str(product.id) #str because of {'3': 4}

        #Update the dictionary
        #Delete from dictionary
        if product_id  in self.cart:
            del self.cart[product_id] #Delete if the product id is there

            #Update the session
            self.session.modified = True


    def cart_total(self):

        #Get product ids
        product_ids = self.cart.keys()

        #Lookup keys in our products db model
        products = Product.objects.filter(id__in=product_ids)

        #Get quanitites from cart
        cart = self.cart #{'3': 4, '4':1}

        #Start counting at 0
        total = 0

        # {'3': 4, '4':1}  # Value is the quantity
        for key, value in cart.items():
            key = int(key) #Convert key string as doing math
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total





