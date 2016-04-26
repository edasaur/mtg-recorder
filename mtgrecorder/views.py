from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import CustomUserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from models import Player
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
#def loggedin(request):
#    return render(request, 'registration/loggedin.html', context={'username': request.user.username})

def register(request):
    #user = User(username="", password="")
    form_user = CustomUserCreationForm()#instance=user)
    ProfileInlineFormset = inlineformset_factory(User, Player, fields=('fun_fact',))
    formset = ProfileInlineFormset()#instance=user)
    if request.method == 'POST':
        form_user = CustomUserCreationForm(request.POST)#, instance=user)
        formset = ProfileInlineFormset(request.POST)#, instance=user)
        if form_user.is_valid():
            created_user = form_user.save(commit=False)
            formset = ProfileInlineFormset(request.POST, instance=created_user)
            if formset.is_valid():
                created_user.save()
                #formset.save()
                return HttpResponseRedirect('/register/complete')
    token = {}
    token.update(csrf(request))
    token['noodle_form'] = form_user
    token['formset'] = formset
    return render(request, 'registration/registration_form.html', context=token)

def registration_complete(request):
    return render(request, 'registration/registration_complete.html')

@login_required(login_url='/login/')
def welcome(request):
    return render(request, 'registration/loggedin.html', context={'username': request.user.username})
