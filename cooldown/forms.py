from django import forms
from cooldown.models import *

class CharacterSelect(forms.Form):
    def __init__(self,*args,**kwargs):
        self.uid = kwargs.pop('user')
        super(CharacterSelect,self).__init__(*args,**kwargs)
        self.fields['name'].queryset = Character.objects.filter(user=self.uid).all()
    name = forms.ModelChoiceField(queryset=None)

class CreateCharacterForm(forms.Form):
    name = forms.CharField(label="Character Name")
    char_class = forms.CharField(label="Character Class",required=False)

class AddSpellForm(forms.Form):
    name = forms.CharField(label="Enter Spell name")
    level = forms.IntegerField(label="Enter Spell level")

class AddItemForm(forms.Form):
    name = forms.CharField(label="Enter item or ability name")
    uses = forms.IntegerField(label="Enter number of uses")
    type = forms.ChoiceField(choices = [(0,"One time user item ( like a potion)"),(1,"rechargable magic item"),(2,"Daily ability or power")])
