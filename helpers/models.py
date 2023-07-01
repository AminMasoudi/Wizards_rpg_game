
from socket import AddressFamily, SocketKind, socket, getdefaulttimeout
from .settings import BUFFER_SIZE
import time
import json
class Sock(socket):
    def __init__(self, family: AddressFamily | int = -1, type: SocketKind | int = -1, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(family, type, proto, fileno)


    def send_msg(self, msg:str):
        
            msg = msg.encode()
            l = str(len(msg)).encode()
            self.send(l)
            time.sleep(0.5)
            self.send(msg)
            return True
    
    def send_command(self, command, args):
        com = {
            "command":command,
            "args": args    
        }

        com         = json.dumps(com).encode()
        comm_len    = str(len(com)).encode()

        self.send(comm_len)
        time.sleep(0.5)
        self.send(com)


    def recv_command(self):
        try:
            len_of_data = self.recv(BUFFER_SIZE).decode()
            command     = self.recv(int(len_of_data))
            command     = json.loads(command)
            
            return command

        except:

            return False



    def recv_msg(self):
        try:
            print(1)
            len_of_msg = self.recv(BUFFER_SIZE).decode()
            print(2)
            msg = self.recv(int(len_of_msg)).decode()
            print(msg)
            return msg
        except:
            pass

    def accept(self):
        fd, addr = self._accept()
        sock = Sock(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr

