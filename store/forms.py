from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last Name", max_length=100)
    username = forms.CharField(label="Username", max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')