from socket import gethostbyname, gethostname
SERVER_PORT = 4441
SERVER_IP = gethostbyname(gethostname())

BUFFER_SIZE = 64