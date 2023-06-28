from helpers.models import Sock
from .models import Game, User

ON_GOING_GAMES = []
PENDING_GAMES = []


def manage_connection(client: Sock, addr):
    client.send_msg(b"AT")
    hand_shake = client.recv_msg()
    if hand_shake != "OK":
        print("[ERROR]: connection failed to maintain")
        client.close()

    user = User(client)
    if PENDING_GAMES:
        game = PENDING_GAMES[0]
        PENDING_GAMES = PENDING_GAMES[1:]
        game.players.append(user)
        game.start()
    else:
        game = Game()
        game.players.append(user)
        user.socket.send_msg("game_status : 'pending' ")