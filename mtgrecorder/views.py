from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm
from forms import ScoreRequestForm, ConfirmRequestForm, TournamentCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Player
from models import Match, ScoreRequest, Tournament
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
    #Gathering info on match requests
    scoreq_verifications = list(ScoreRequest.objects.filter(verified=1).filter(player2=user.player))
    scoreq_ids = map(lambda x: x.id, scoreq_verifications)
    urls = map(lambda x: '/match/'+str(x), scoreq_ids)
    opponent_ids = map(lambda x: x.player1_id, scoreq_verifications)
    opponent_usernames = map(lambda x: x.player1.user.username, scoreq_verifications)
    wins = map(lambda x: x.loss, scoreq_verifications)
    loss = map(lambda x: x.wins, scoreq_verifications)
    ties = map(lambda x: x.ties, scoreq_verifications)
    opponent_names = map(lambda x:list(Player.objects.filter(id=x))[0].user.first_name+' '+list(Player.objects.filter(id=x))[0].user.last_name, opponent_ids)
    scoreRequests = []
    for i in xrange(len(opponent_ids)):
        scoreRequests.append((opponent_names[i], wins[i], loss[i], ties[i], urls[i], ConfirmRequestForm(instance=scoreq_verifications[i]), opponent_usernames[i]))
    #Gathering info on which tournaments you're in
    tournaments_in = Tournament.objects.filter(participants__DCI=request.user.player.DCI)
    print tournaments_in
    con = {}
    con.update(csrf(request))
    con['first_name'] = user.first_name+' '+user.last_name
    con['opponents'] = scoreRequests
    con['username'] = user.username
    con['profile_url'] = '/profile/'+user.username
    con['tournaments_in'] = tournaments_in
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
            p2_wins = match.loss
            con = {'match':match, 'player2_name':player2_name, 'p1_wins':p1_wins, 'ties':ties, 'p2_wins':p2_wins}
            con['profile_url'] = '/profile/'+request.user.username
            return render(request, 'registration/verification_requested.html', context=con)
    else:
        form = ScoreRequestForm(current_user=request.user, initial={'player1': request.user.player})#request.user)
    return render(request, 'registration/request_verification.html', context={'form':form, 'first_name':request.user.first_name, 'last_name':request.user.last_name, 'profile_url':'/profile/'+request.user.username})

@login_required(login_url='/login/')
def confirm_match(request, req_id=None):
    if request.method == "POST":
        if req_id is not None:
            try:
                sr = ScoreRequest.objects.get(id=req_id)
            except:
                return HttpResponseRedirect('/welcome/')
            form = ConfirmRequestForm(request.POST, instance=sr)
            print form
            if form.is_valid() and sr.player2.user.username == request.user.username: #and needs to verify player2 is current player lol
                form.save()
                if int(request.POST['verified']) == 2:
                    #Save fields into a Match object now
                    match = Match()
                    match.player1 = sr.player1
                    match.player2 = sr.player2
                    match.wins = sr.wins
                    match.loss = sr.loss
                    match.ties = sr.ties
                    match.tournament = sr.tournament
                    match.save()
                return HttpResponseRedirect('/welcome/') 
            return HttpResponseRedirect('/welcome/')
    else:
        print "Only POST requests for now"
        return HttpResponseRedirect('/welcome/')

def wlt(player, match):
    """ Returns a tuple containing the results for player
    <OUTCOME>, <WINS>, <LOSS>, <TIES>

    <OUTCOME> is    True if player won the match
                    False if player lost the match
                    None if player tied the match
    """
    assert player == match.player1 or player == match.player2, "func wlt views"
    if player == match.player1:
        wins = match.wins
        loss = match.loss
        opp = match.player2
    else:
        wins = match.loss
        loss = match.wins
        opp = match.player1
    ties = match.ties
    return wins > loss if wins != loss else None, wins, loss, ties, opp

@login_required(login_url='/login/')
def add_tournament(request):
    if request.method == "POST":
        form = TournamentCreationForm(request.user, request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/welcome/')
    else:
        form=TournamentCreationForm(current_user=request.user)
    return render(request, 'tournament/request_verification.html', context={'form':form,})

@login_required(login_url='/login/')
def profile(request, username):
    player = User.objects.filter(username=username)
    assert len(player) == 1, "More than one player found with username"
    player = player[0].player
    matches = Match.objects.filter(Q(player1=player)|Q(player2=player))
    matches = matches.order_by('tournament', '-date_submitted')
    grouped = []
    last_tournament = None
    for match in matches:
        if match.tournament != last_tournament:
            if last_tournament is not None:
                grouped.append(tournament)
            tournament = {
                'name':match.tournament,
                'matches':[],
                'm_wins':0, 'm_loss':0, 'm_ties':0,
                'g_wins':0, 'g_loss':0, 'g_ties':0,
            }
            last_tournament = match.tournament
        outcome, wins, loss, ties, opp = wlt(player, match)
        tournament['g_wins'] += wins
        tournament['g_loss'] += loss
        tournament['g_ties'] += ties
        tournament[{True:'m_wins', False:'m_loss', None:'m_ties'}[outcome]] += 1
        clean_match = {
            'opponent':opp,
            'wins':wins,
            'loss':loss,
            'ties':ties,
            'outcome': {True:'Win', False:'Lose', None:'Tie'}[outcome],
        }
        tournament['matches'].append(clean_match)
    if len(matches):
        grouped.append(tournament)
    
    context = {
        'g_wins':0, 'g_loss':0, 'g_ties':0,
        'm_wins':0, 'm_loss':0, 'm_ties':0,
    }
    
    for tournament in grouped:
        for key in context:
            context[key] += tournament[key]
    
    context['player'] = player
    context['tournaments'] = grouped
    context['profile_url'] = '/profile/'+request.user.username
    return render(request, 'profile/profile.html', context)



