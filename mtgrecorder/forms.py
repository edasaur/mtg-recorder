from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import Player, Match
from django import forms

class CustomUserCreationForm(UserCreationForm):#forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",  "username") 
    
class MatchRequestForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ("player1", "player2", "wins", "loss", "ties", "tournament")
