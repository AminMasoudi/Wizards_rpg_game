import threading
from helpers.settings import SERVER_PORT, SERVER_IP
from helpers.models import Sock
from .helpers import manage_connection


server = Sock()
server.bind((SERVER_IP, SERVER_PORT))
server.listen()
print(f"[RUNNING]: server is running on {SERVER_IP}:{SERVER_PORT}")


while True:
    client, addr = server.accept()
    print(f"[NEW CONNECTION]: connected to {addr}")
    threading.Thread(target=manage_connection, args=(client, addr))
    print(f"[ACTIVATED] active client: {threading.active_count()}")

    