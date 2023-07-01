from helpers.settings import *
from helpers.models import Sock

def main():
    connection = server_connection()
    # while True:
    #     print(connection.recv_msg())
    

def server_connection():
    connection = Sock()
    connection.connect((SERVER_IP, SERVER_PORT))
    connection.send_command("foo", args=[])
    
    
if __name__ == "__main__":
    main()