from .models import UserCheckout
from django import forms

class UserCheckoutForm(forms.ModelForm):
    
    class Meta:
        model = UserCheckout
        fields = "fullname","telephone", "email", "shipping_address", "payment_method","email"

class UserFormx(forms.Form):
    fullname = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=15)
    email = forms.EmailField(max_length=100)
    shipping_address = forms.CharField(max_length=100)
    payment_method = forms.CharField(max_length=100)
    
