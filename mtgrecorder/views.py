from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Player
from models import Match
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.db.models import Q
#def loggedin(request):
#    return render(request, 'registration/loggedin.html', context={'username': request.user.username})

def register(request):
    #user = User(username="", password="")
    #form_user = CustomUserCreationForm()#instance=user)
    #ProfileInlineFormset = inlineformset_factory(User, Player, fields=('DCI',))
    #formset = ProfileInlineFormset()#instance=user)
    if request.method == 'POST':
        form_user = CustomUserCreationForm(request.POST)#, instance=user)
        #formset = ProfileInlineFormset(request.POST)#, instance=user)
        if form_user.is_valid():
            form_user.save()
            #formset = ProfileInlineFormset(request.POST, instance=created_user)
            #if formset.is_valid():
            #    created_user.save()
                #formset.save()
            return HttpResponseRedirect('/register/complete')
    else:
        form_user = CustomUserCreationForm()
    token = {}
    token.update(csrf(request))
    token['noodle_form'] = form_user
    #token['formset'] = formset
    return render(request, 'registration/registration_form.html', context=token)

def registration_complete(request):
    return render(request, 'registration/registration_complete.html')

@login_required(login_url='/login/')
def welcome(request):
    user = request.user
    match_verifications = Match.objects.filter(verified=False).filter(Q(player1=user.player) | Q(player2=user.player))
    return render(request, 'registration/loggedin.html', context={'first_name': user.get_full_name(), 'unverified_matches': match_verifications})
