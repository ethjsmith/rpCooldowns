from django.db import models
from django.contrib.auth.models import User
# creating the database looks like this
#`python manage.py makemigrations cooldown`
#`python manage.py migrate `
#`python manage.py shell`

class Character(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}"

class Spell(models.Model):
    id = models.AutoField(primary_key=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.TextField()
    spell_level = models.IntegerField()
    # cooldown can be derived from level, which makes more sense. I want to keep a more consistent naming convention for this version
    current_cooldown = models.IntegerField()
    def check_if_ready(self): # checks if the cooldown of the spell is currently zero
        if self.current_cooldown == 0:
            return True
        return False
    def reset(self):
        self.current_cooldown = 0
    def take_turn(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
    def use_spell(self):
        self.current_cooldown = self.spell_level +1 # plus 1 for the first turn when you cast the spell


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
    def __str__(self):
        return f"{self.name}"
    def check_if_usable(self): # checks if the item currently has any uses.
        if self.current_uses > 0:
            return True
        return False
    def rest(self):
        if self.type == 1:
            self.current_uses = self.max_uses
    def recharge(self,charges):
        self.current_uses += charges
        if self.current_uses > self.max_uses:
            self.current_uses = self.max_uses
    def use(self):
        self.current_uses -= 1
        if self.current_uses <= 0 and self.type == 0:
            return 1
        return 0
