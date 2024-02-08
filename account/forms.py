from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from django.contrib.auth.models import User
from .models import  ClientAccount
from .constants import GENDER_TYPE

class UserRegistrationForm(UserCreationForm):
    first_name=forms.CharField(label='First Name', widget=forms.TextInput(attrs={'id':'required'}))
    last_name=forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'id':'required'}))
    email=forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'id':'required'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
   
    class Meta:
        model=ClientAccount
        fields=['username','first_name','last_name','email','gender','birth_date']




class MakeAdminForm(forms.Form):
    # user_id=forms.IntegerField()
    user_to_make_admin = forms.ModelChoiceField(queryset=ClientAccount.objects.all())
    # user_to_make_admin = forms.ModelChoiceField()

class UserUpdateForm(UserChangeForm):
    password=None   
    class Meta:
        model=ClientAccount
        fields=['username','first_name','last_name','email','birth_date','social_media_links','profile_image']

 