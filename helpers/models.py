from _socket import _RetAddress as _RetAddress
import socket
from socket import AddressFamily, SocketKind, socket, getdefaulttimeout
from helpers.settings import BUFFER_SIZE


class Sock(socket):
    def __init__(self, family: AddressFamily | int = -1, type: SocketKind | int = -1, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(family, type, proto, fileno)


    def send_msg(self, msg:str):
        try:
            msg = msg.encode()
            self.send(len(msg))
            self.send(msg)
            return True
        except:
            return False
        
    def recv_msg(self):
        len_of_msg = self.recv(BUFFER_SIZE)
        msg = self.recv(len_of_msg).decode()
        return msg

    def accept(self) -> tuple[socket, _RetAddress]:
        fd, addr = self._accept()
        sock = Sock(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr

