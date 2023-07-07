from django.contrib.auth.models import User
from django.db import models
import random
# Create your models here.


class Roles(models.Model):
    name    = models.CharField(max_length=15)
    power   = models.PositiveIntegerField(default=5)
    magic   = models.PositiveIntegerField(default=5)
    mrr     = models.PositiveIntegerField(default=10)

    ef_defend   = models.PositiveIntegerField(default=50)
    ef_hit      = models.PositiveIntegerField(default=50)
    ef_magic    = models.PositiveIntegerField(default=50)

    def dict(self):
        content = {
            "name" : self.name,
            "magic": self.magic,
            "power": self.power,
            "mrr"  : self.mrr,

            "re_life"   : 100,
            "ef_defend" : self.ef_defend,
            "ef_hit"    : self.ef_hit,
            "ef_magic"  : self.ef_magic
        }
        return content
    



class Game(models.Model):
    status     = models.CharField(max_length=10, default="Pending")



class Player(User):
    username = models.CharField(
    max_length=15,
    unique=True,
    ),
    role = models.JSONField(null=True)
    last_action = models.CharField(max_length=10, default="")
    password = 1234
    game = models.ManyToManyField(Game, blank=True, related_name="player")

    def set_role(self, role_dict):
        self.role = role_dict
        self.save()

    def calculate(self, o_actor):
        defend = 0
        if o_actor.last_action == "attack":
            self.role["re_life"] -= o_actor.role["power"]
            
        elif self.last_action == "defend" and o_actor.last_action == "magic":
            to_defend = self.role["ef_defend"] // 100

            defend = random.choices([0,1],[1- to_defend, to_defend])

            if not defend:
                self.role["re_life"] -= o_actor.role["ef_magic"]

        self.save()