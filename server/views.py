"""
HERE is our views like django :))

"""
from .models import Player, Game, Role
from .consts import PLAYERS, ROLES

ON_GOING_GAMES  = []
PENDING_GAMES   = []

def foo(*args):
    print("FOOOOOOOOOOOOOO")


def join(*args):
    args = args[0]
    global PENDING_GAMES
    socket = args["socket"]
    player = Player(socket)
    PLAYERS.append(player)

    if PENDING_GAMES:
        game = PENDING_GAMES[0]
        PENDING_GAMES = PENDING_GAMES[1:]
        game.player2 = player
        player.game = game
        game.start()  #FIXME should be with thread??

    else:
        game = Game()
        game.player1 = player
        player.game = game
        PENDING_GAMES.append(game)
        socket.send_json({
            "type" : "new_status",
            "status" : "Pending"
        })


def submit_role(args):
    client = args["socket"]
    role = args["role"]
    player = list(filter(lambda pl : pl.socket == client , PLAYERS))[0]
    print(player)
    if role in ROLES:
        player.role = Role(role)
    

def get_info(args):
    client = args["socket"]
    player = list(filter(lambda pl : pl.socket == client , PLAYERS))[0]
    game: Game = player.game
    player_b = game.player1 if game.player1 != player else game.player2
    print(player.role)
    content = {
        "player" : player.role.ser(),
        "player_b" :  player_b.role.ser(),
    }
    client.send_json({
        "type" : "game_info",
        "content" : content
    })


def action(args):
    client = args["socket"]
    player = list(filter(lambda pl : pl.socket == client , PLAYERS))[0]
    if not player.last_action:
        player.last_action = args["action"]
        