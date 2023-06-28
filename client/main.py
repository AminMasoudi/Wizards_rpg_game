from helpers.settings import *
from helpers.models import Sock

def main():
    ...



def server_connection():
    connection = Sock()
    connection.connect((SERVER_IP, SERVER_PORT))
    #hand shake
    if connection.recv_msg() != "AT":
        print("[ERROR] Failed to connect")
        connection.close()
        raise ConnectionError
    else:
        connection.send_msg("OK")
    
    
if __name__ == "__main__":
    main()