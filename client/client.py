from helpers.models import Sock
from helpers.settings import *
import threading
from consts import set_page

def server_connection():
    connection = Sock()
    connection.status = "Connecting ..."
    connection.connect((SERVER_IP, SERVER_PORT))
    connection.send_command("foo", args={})
    threading.Thread(target=listen, args=(connection,)).start()
    return connection


def join_to_room(connection: Sock):
    connection.send_command("join", args={})

def listen(connection):
    while True:
        msg = connection.recv_json()

        if msg["type"] == "new_status":
            connection.status = msg["status"]
        
        if msg["type"] == "ask_role":
            print("im here")
            roles = msg["roles"]
            set_page("ask_role")
            connection.roles = roles