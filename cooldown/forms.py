from django import forms
from cooldown.models import *

class CharacterSelect(forms.Form):
    name = forms.ModelChoiceField(queryset=Character.objects.all())

class CreateCharacterForm(forms.Form):
    name = forms.CharField(label="Character Name")
    char_class = forms.CharField(label="Character Class",required=False)
