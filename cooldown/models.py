from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Spell(models.Model):
    id = models.AutoField(primary_key=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.TextField()
    spell_level = models.IntegerField()
    # cooldown can be derived from level, which makes more sense. I want to keep a more consistent naming convention for this version
    current_cooldown = models.IntegerField()
    def check_if_ready(self): # checks if the cooldown of the spell is currently zero
        if current_cooldown == 0:
            return True
        return False
    def reset(self):
        current_cooldown = 0
    def take_turn(self):
        if current_cooldown > 0:
            current_cooldown -= 1
    def use_spell(self):
        current_cooldown = spell_level +1 # plus 1 for the first turn when you cast the spell


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.TextField()
    type = models.IntegerField()
    # type 0- = potions/ consumables
    # type 1 = daily limited abilities
    # type 2+ = objects with charges, that are not automatically recharged.
    # TODO other types of magic items, like regenerating charge items... ( is this in 3.5? I haven't seen it )
    max_uses = models.IntegerField()
    current_uses = models.IntegerField()
    def check_if_usable(self): # checks if the item currently has any uses.
        if current_uses > 0:
            return True
        return False
    def rest(self):
        if type == 1:
            current_uses = max_uses
    def recharge(self,charges):
        current_uses += charges
        if current_uses > max_uses:
            current_uses = max_uses
    def use(self):
        current_uses -= 1
        # I don't know if I should define deletion behavior here
        if current_uses == 0 and type == 0:
            print("kill this item ") # placeholder
