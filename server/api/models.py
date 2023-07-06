from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Player(User):
    username = models.CharField(
    max_length=15,
    unique=True,
    ),
    password = 1234
    


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
            "power": self.power,
            "magic": self.magic,
            "mrr"  : self.mrr,

            "ef_defend" : self.ef_defend,
            "ef_hit"    : self.ef_hit,
            "ef_magic"  : self.ef_magic
        }
        return content