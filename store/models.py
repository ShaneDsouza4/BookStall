from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create Customer Profile
class Profile(models.Model):
    #Associate one profile with one User
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Delete associated Profile if User account deleted
    date_modified = models.DateTimeField(User, auto_now=True)

    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username #Will be displayed in /admin

# Create User profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# AUtomate
post_save.connect(create_profile, sender=User)




# Category Model
class Category(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

# Customer Model
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(default="", blank=True, null=True)
    image = models.ImageField(upload_to="uploads/products")
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

# Order Model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default="", blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name