from rest_framework import serializers
from .models import Roles

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"