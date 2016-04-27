from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm
from forms import MatchRequestForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Player
from models import Match
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, Q
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
    return render(request, 'registration/loggedin.html', context={'first_name': user.get_full_name()})

@login_required(login_url='/login/')
def request_verification(request):
    if request.method == "POST":
        form = MatchRequestForm(request.POST)
        if form.is_valid():
            match = form.save()
            player2 = Player.objects.get(id=match.player2)
            player2_name = player2.first_name + ' ' + player2.last_name
            return render(request, 'verification_requested.html', context={'match':match, 'player2_name':player2_name})
    else:
        form = MatchRequestForm()
    return render(request, 'request_verification.html', context={'form':form})

