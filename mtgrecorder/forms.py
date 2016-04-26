from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import Player
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
       
class CustomPlayerCreationForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ("fun_fact",) 
    def save(self, commit=True):
        player = super(CustomPlayerCreationForm, self).save(commit=False)
        player.fun_fact = self.cleaned_data["fun_fact"]
        if commit:
            player.save()
        return player
