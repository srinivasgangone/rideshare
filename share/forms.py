from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Ride

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        

class RideForm(forms.ModelForm):

    class Meta:
        model = Ride
        exclude = ("customer", "id",)

class SearchRideForm(forms.ModelForm):

    class Meta:
        model = Ride
        fields = ("departure", "destination",)


class RideForm(forms.ModelForm):

    class Meta:
        model = Ride
        exclude = ['_id', 'created_at', 'driver', 'customer', "id",]