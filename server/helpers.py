from helpers.models import Sock

def manage_connection(client: Sock, addr):
    client.send_msg(b"AT")
    hand_shake = client.recv(2).decode()
    if hand_shake != "OK":
        print("[ERROR]: connection failed to maintain")
        client.close()

