
from socket import AddressFamily, SocketKind, socket, getdefaulttimeout
from .settings import BUFFER_SIZE
import time
import json

def try_decorator(f):
    def wraper(args):
        try:
            result = f(args)
        except Exception as e:
            #TODO log
            print("[ERROR LOG]: ", e)
            return False
        return result
    return wraper


class Sock(socket):
    def __init__(self, family: AddressFamily | int = -1, type: SocketKind | int = -1, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(family, type, proto, fileno)


    def send_msg(self, msg:str):
        """ takes an `str` and first send the len then sends the `msg`"""

        msg = msg.encode()
        l   = str(len(msg)).encode()
        self.send(l)
        time.sleep(0.5)
        self.send(msg)


    def send_command(self, command : str, args : list):
        """takes a command name as `command` and needed `args`"""
        com = {
            "command":command,
            "args": args    
        }
        com         = json.dumps(com).encode()
        comm_len    = str(len(com)).encode()
        self.send(comm_len)
        time.sleep(0.5)
        self.send(com)

    @try_decorator
    def recv_command(self):
        len_of_data = self.recv(BUFFER_SIZE).decode()
        command     = self.recv(int(len_of_data))
        command     = json.loads(command)
        
        return command

    @try_decorator
    def recv_msg(self):
    
        len_of_msg  = self.recv(BUFFER_SIZE).decode()
        msg         = self.recv(int(len_of_msg)).decode()
        return msg

    def accept(self):
        fd, addr = self._accept()
        sock    = Sock(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr

