from helpers.models import Sock
from .models import Game, User
from . import views
import threading

websocket_pattern = {
    "command" : "function",
    "foo"     : views.foo,
    
}

ON_GOING_GAMES  = []
PENDING_GAMES   = []

def manage_connection(client, addr):

    while True:
        command = client.recv_command()
        if command:
            function = websocket_pattern[command["command"]]
            threading.Thread(target=function, args=command["args"]).start()
            
        else: 
            print(f"[DETACHED]: connection lost with {addr}")
            client.close()
            break
            




#{"command" : "command_name",
# "args": [
#       arg1,
#       arg2,
# ]}