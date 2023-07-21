from django.contrib import admin
from .models import Player, Roles, Game
# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "power", "magic"]


admin.site.register(Player)
admin.site.register(Roles,RoleAdmin)
admin.site.register(Game)