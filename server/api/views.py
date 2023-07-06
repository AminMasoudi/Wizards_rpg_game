from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from .models import Player, Roles
from .serializers import RoleSerializer

# Create your views here.


@api_view(["POST"])
def auth(request):
    username = request.POST.get("username", False)
    if username:
        _ = Player.objects.filter(username=username).all()
        if not _ :
            user = Player.objects.create(username = username)
            login(request, user)
            return Response({"result" : "ok"})
    return Response ({"result" : "failed"})
        

@api_view(["GET"])
def get_roles(request):
    roles = Roles.objects.all()
    ser_roles = RoleSerializer(roles, many=True)
    return Response(ser_roles.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def define_role(request):
    player = Player.objects.get(username=request.user.username)
    role = Roles.objects.get(id=request.POST["id"])
    player.remaining_life = 100
    player.role = role.dict()
    return Response({"result" : "ok"})
