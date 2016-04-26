from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm, CustomPlayerCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Player
#def loggedin(request):
#    return render(request, 'registration/loggedin.html', context={'username': request.user.username})

def register(request):
    if request.method == 'POST':
        form_user = CustomUserCreationForm(request.POST)
        form_player = CustomPlayerCreationForm(request.POST)
        if (form_user.is_valid() and form_player.is_valid()):
            user = form_user.save()
            player = form_player.save(commit=False)
            player.user = user
            player.save()
            return HttpResponseRedirect('/register/complete')
    else:
        form_user = CustomUserCreationForm()
        form_player = CustomPlayerCreationForm()
    token = {}
    token.update(csrf(request))
    token['form_user'] = form_user
    token['form_player'] = form_player
    return render(request, 'registration/registration_form.html', context=token)

def registration_complete(request):
    return render(request, 'registration/registration_complete.html')

@login_required(login_url='/login/')
def welcome(request):
    return render(request, 'registration/loggedin.html', context={'username': request.user.username})
