from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms

from store.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last Name", max_length=100)
    username = forms.CharField(label="Username", max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UpdateUserForm(UserChangeForm):
    password = None #Hide password stuff

    #Other fields
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last Name", max_length=100)
    username = forms.CharField(label="Username", max_length=150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User

        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        required=False,
    )
    address1 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}),
        required=False,
    )
    address2 = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}),
        required=False,
    )
    city = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        required=False,
    )
    state = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
        required=False,
    )
    zipcode = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
        required=False,
    )
    country = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country')