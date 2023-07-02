from socket import gethostbyname, gethostname
SERVER_PORT = 4444
SERVER_IP = gethostbyname(gethostname())

BUFFER_SIZE = 64