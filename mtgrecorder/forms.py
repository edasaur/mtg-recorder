from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import Player
from django import forms

class CustomUserCreationForm(UserCreationForm):#forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",  "username") 
