from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse_lazy

from cooldown.models import *
import datetime, threading  # not sure I need these
from cooldown.decorators import *
from cooldown.forms import *

class SignUpView(generic.CreateView): #TODO rework this
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
@character_selected
def dashboard(request):
    return render(request,"spellpage.html")

def character(request):
    if request.method == "POST":
        addform = CreateCharacterForm(request.POST)
        if addform.is_valid():
            newchar = Character(name = addform.cleaned_data['name'],user=request.user).save() # maybe this works :)

    addform = CreateCharacterForm()
    selectform = CharacterSelect()
    return render(request,"chars.html",{"addform":addform,"selectform":selectform})

def use_item(request,item):
    return "test"

def recharge_item(request):
    return "test"

def cast_spell(request,spell):
    return "test"

def take_turn(request):
    return "test"

def rest(request):
    return "test"

def a(request):
    return "test"

def admin(request):
    return "test"

def delete(request,type,id):
    return "test"
