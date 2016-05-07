from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from models import Player, ScoreRequest
from django import forms

class CustomUserCreationForm(UserCreationForm):#forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",  "username") 
    
class ScoreRequestForm(forms.ModelForm):
    def __init__(self, current_user=None, *args, **kwargs):
        super(ScoreRequestForm, self).__init__(*args, **kwargs)
        #print args[0].username, args[0].first_name, args[0].last_name, args[0]
        if current_user is not None:
            self.fields['player1'].queryset = Player.objects.filter(user=current_user)
            self.fields['player2'].queryset = Player.objects.exclude(user=current_user)
    #def clean_player1(self):
    #    return self.instance.player1   class Meta:
    class Meta:
        model = ScoreRequest
        fields = ("player1", "player2", "wins", "loss", "ties", "tournament")
SELECT_CHOICES = (
    (2, 'Confirm'),
    (3, 'Decline'),
)

class ConfirmRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConfirmRequestForm, self).__init__(*args, **kwargs)
        self.fields['verified'] = forms.ChoiceField(label=u'', choices=SELECT_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = ScoreRequest
        fields = ("verified",)

