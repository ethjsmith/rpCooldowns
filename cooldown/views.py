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
                return redirect("/")
    addform = CreateCharacterForm()
    selectform = CharacterSelect(user=request.user)
    return render(request,"chars.html",{"addform":addform,"selectform":selectform})

def use_item(request,item):
    i = Item.objects.filter(id=item).first()
    z = i.use()
    if z == 1:
        i.delete()
    else:
        i.save()
    return redirect("/")

def recharge_item(request):
    if request.method == "POST":
        rechargeform = RechargeForm(request.POST,character=Character.objects.filter(name=request.session['character']).first())
        if rechargeform.is_valid():
            itm = rechargeform.cleaned_data['item']
            itm.recharge(rechargeform.cleaned_data['number'])
            itm.save()
        return redirect("/")
    rechargeform = RechargeForm(request.POST,character=Character.objects.filter(name=request.session['character']).first())
    return render(request,"recharge.html",{"rechargeform":rechargeform})

def cast_spell(request,spell): # maybe :)
    s = Spell.objects.filter(id=spell).first()
    s.use_spell()
    s.save()
    return redirect("/")

def take_turn(request):
    character = Character.objects.filter(name=request.session['character']).first()
    spells = Spell.objects.filter(character=character)
    for spell in spells:
        spell.take_turn()
        spell.save()
    return redirect("/")

def rest(request):
    character = Character.objects.filter(name=request.session['character']).first()
    spells = Spell.objects.filter(character=character)
    items = Item.objects.filter(character=character)
    for spell in spells:
        spell.reset()
        spell.save()
    for item in items:
        item.rest()
        item.save()
    return redirect("/")

def a(request): # selecting like this is simpler, but less usable, might be better to do some complex data structure
    u = User.objects.all()
    c = Character.objects.all()
    s = Spell.objects.all()
    i = Item.objects.all()
    return render(request,"admin.html",{"users":u,"characters":c,"spells":s,"items":i})

def admin(request):# I Don't know what this is supposed to do
    return "more admin view"

def delete(request,type,id):
    if type == "": # like this, really?
        print("select")
    return redirect("/a")
