from django import forms


from django.contrib.auth.models import User
from .models import  ClientAccount
from .models import  ContactUs
class ContactForm(forms.ModelForm):
   
    class Meta:
        model=ContactUs
        fields='__all__'


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 
                                            'style': 'border-radius: 16px; border: 1px solid black;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 
                                              'style': 'border-radius: 16px; border: 1px solid black;'}),
          
        }