from helpers.models import Sock
from helpers.settings import *
import threading
import time
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

def submit_role(connection, role):
    print(role)
    connection.sended = True
    connection.send_command("submit_role", args={"role": role})

def submit_action(connection, action):
    print(f"[SENDING ACTION] sending {action} as action")
    connection.send_action = True
    connection.send_command("post_action", args={"action" : action})
    


def listen(connection):
    while True:
        msg = connection.recv_json()

        if msg["type"] == "new_status":
            connection.status = msg["status"]
            if msg["status"] == "game_inited":
                print("[initing game]")
                connection.send_command("ask_info",{})
                time.sleep(1)
                set_page("game")
        
        if msg["type"] == "ask_role":
            roles = msg["roles"]
            connection.roles = roles
            connection.sended = False
            set_page("ask_role")

        if msg["type"] == "game_info":
            connection.game_data = msg["content"]
            connection.send_action = False
