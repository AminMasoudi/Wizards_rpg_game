from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from .models import Player, Roles, Game
from .serializers import RoleSerializer, GameSerializer, PlayerSerializer

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
    player.set_role = role.dict()
    return Response({"result" : "ok"})



@api_view(["GET"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_game(request):
    player = Player.objects.get(username=request.user.username)
    game = Game.objects.filter(status="Pending").first()
    if game:
        game.status = "started"
        game.save()
    else :
        game = Game.objects.create()
    
    player.game.add(game)
    ser_game = GameSerializer(game)
    return Response(ser_game.data)
    


@api_view(["GET"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def game_info(request):
    player = Player.objects.get(username=request.user.username)
    game = player.game.first()
    tmp = {}
    content = GameSerializer(game).data
    for p in content["player"]:
        if p == player.pk:
            tmp["u_player"] = PlayerSerializer(player).data
        else:
            op = Player.objects.get(pk=p)
            tmp["o_player"] = PlayerSerializer(op).data
    content["player"] = tmp
    return Response(content)