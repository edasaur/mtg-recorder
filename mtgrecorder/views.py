from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm
from forms import ScoreRequestForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Player
from models import Match, ScoreRequest
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
    match_verifications = list(ScoreRequest.objects.filter(verified=False).filter(player2=user.player))
    match_ids = map(lambda x: x.id, match_verifications)
    opponent_ids = map(lambda x: x.player1_id,match_verifications)
    wins = map(lambda x: x.loss, match_verifications)
    loss = map(lambda x: x.wins, match_verifications)
    ties = map(lambda x: x.ties, match_verifications)
    opponent_names = map(lambda x:list(Player.objects.filter(id=x))[0].user.first_name+' '+list(Player.objects.filter(id=x))[0].user.last_name, opponent_ids)
    total = []
    for i in xrange(len(opponent_ids)):
        total.append((opponent_names[i], wins[i], loss[i], ties[i], match_ids[i]))
    con = {}
    con.update(csrf(request))
    con['first_name'] = user.first_name+' '+user.last_name
    con['opponents'] = total
    return render(request, 'registration/loggedin.html', context=con)

@login_required(login_url='/login/')
def request_verification(request):
    if request.method == "POST":
        form = ScoreRequestForm(request.user, request.POST)
        if form.is_valid():
            match = form.save()
            player2 = Player.objects.get(id=match.player2_id)
            player2_name = player2.user.first_name + ' ' + player2.user.last_name
            p1_wins = match.wins
            ties = match.ties
            p1_loss = match.loss
            con = {'match':match, 'player2_name':player2_name, 'p1_wins':p1_wins, 'ties':ties, 'p1_loss':p1_loss}
            return render(request, 'registration/verification_requested.html', context=con)
    else:
        form = ScoreRequestForm(current_user=request.user, initial={'player1': request.user.player})#request.user)
    return render(request, 'registration/request_verification.html', context={'form':form, 'first_name':request.user.first_name, 'last_name':request.user.last_name})

@login_required(login_url='/login/')
def verify_request(request):
    if request.method == "POST":
        print "OIWEHFPOIWHEFOPWIEHFPOWIEHFPOWEIFH"
        print request.POST        
