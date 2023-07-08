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
    result     = models.JSONField(default=dict)
    round_number= models.SmallIntegerField(default=1)

    def add_result(self):
        ps = self.player.all()
        content = {
            "player1" : ps[0].last_action,
            "player1_life" : ps[0].role["re_life"],

            "player2" : ps[1].last_action,
            "player2_life" : ps[1].role["re_life"],

        }
        try:
            self.result["rounds"][self.round_number] = content
        except:
            self.result["rounds"] = {}
            self.result["rounds"][self.round_number] = content

        self.round_number += 1
        self.save()
    
    def winner(self):
        p1, p2 = self.player.all()
        p1_dead = (p1.role["re_life"] <= 0)
        p2_dead = (p2.role["re_life"] <= 0)
        if p1_dead and p2_dead:
            self.result["winner"] = "EQUAL"
        elif p1_dead:
            self.result["winner"] = p2.username
        else:
            self.result["winner"] = p2.username
        self.save()
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
            
        elif self.last_action == defend:
            to_defend = self.role["ef_defend"] // 100

            defend = random.choices([0,1],[1- to_defend, to_defend])

            if not defend and o_actor.last_action == "magic":
                self.role["re_life"] -= o_actor.role["ef_magic"]

        self.save()