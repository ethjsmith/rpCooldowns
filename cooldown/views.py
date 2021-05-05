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
    character = Character.objects.filter(name=request.session['character']).first()
    if request.method == "POST":
        if request.POST.get("add_spell"):
            add_spell = AddSpellForm(request.POST)
            if add_spell.is_valid():
                Spell(
                character =character,
                name=add_spell.cleaned_data['name'],
                spell_level=add_spell.cleaned_data['level'],
                current_cooldown = 0
                ).save()
        elif request.POST.get("add_item"):
            add_item = AddItemForm(request.POST)
            if add_item.is_valid():
                Item(
                character=character,
                name=add_item.cleaned_data['name'],
                type=add_item.cleaned_data['type'],
                max_uses=add_item.cleaned_data['uses'],
                current_uses=add_item.cleaned_data['uses'],
                ).save()
    add_spell = AddSpellForm()
    add_item = AddItemForm()
    spells = Spell.objects.filter(character=character).all()
    items = Item.objects.filter(character=character).all()
    return render(request,"spellpage.html",{"character":character,"spells":spells,"items":items,"add_spell":add_spell,"add_item":add_item})

def character(request):
    if request.method == "POST":
        if request.POST.get("add_character"):
            addform = CreateCharacterForm(request.POST)
            if addform.is_valid():
                newchar = Character(name = addform.cleaned_data['name'],user=request.user).save()
        elif request.POST.get("select_character"):
            selectform = CharacterSelect(request.POST,user=request.user)
            if selectform.is_valid():
                request.session['character']= selectform.cleaned_data['name'].name
    addform = CreateCharacterForm()
    selectform = CharacterSelect(user=request.user)
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
