from rest_framework import serializers
from .models import Roles, Game, Player

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["pk", "player", "status"]

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["username", "role"]

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["result", "status"]