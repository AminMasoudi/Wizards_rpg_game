class Game():
    
    def __init__(self) -> None:
        self.inited = False
        self.pending = True
        self.players = []

    def init_game(self):
        try:
            b = True
            self.player1 = Player(self.players[0])
            self.player2 = Player(self.players[1])
            b *= self.player1.ask_role()
            b *= self.player2.ask_role()
            b *= self.broadcast("{game_status : 'inited' }")
            self.inited = True
            return b
        except:
            return False

    def broadcast(self, msg):
        try:
            for user in self.players:
                user.socket.send_msg(msg)
                return True
        except:
            return False
    def start(self):
        if self.init_game(): 
            while not self.is_over():
                self.play_round()
        
    def is_over(self):
        #TODO
        ...
    
    def play_round(self):
        #TODO
        ...
    #player 2
    #  

class Role():
    ...

class User():
    def __init__(self, csoc) -> None:
        self.socket = csoc


class Player():
    def __init__(self, user) -> None:
        self.user = user
        self.role = self.user.role

    def ask_role(self):
        ...