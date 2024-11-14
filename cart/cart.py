from django.contrib.sites import requests

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

