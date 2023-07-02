"""
HERE is our views like django :))

"""
from .models import Player, Game
from .consts import PLAYERS

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


