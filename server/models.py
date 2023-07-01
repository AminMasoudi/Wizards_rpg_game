import threading

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
        """
        return `True` if game is over (someone dies or other conditions)
        else return `False`
        """
        #TODO
     
    def play_round(self):
        # TODO
        # - [ ] ask for action
        self.broadcast("action")
        self.player1.ask_action()
        self.player2.ask_action()

        # - [ ] 

    #player 2
    #  



class Role():
    def __init__(self,role_dict) -> None:
        self.name   = role_dict["name"]
        self.magic  = role_dict["magic"]
        self.power  = role_dict["power"]


        self.remaining_life      = 100
        self.effective_defend    = role_dict["e_defend"]
        self.effective_hit       = role_dict["e_hit"]
        self.effective_magic     = role_dict["e_magic"]
        self.magic_recovery_rate = role_dict["MRR"]



class User():
    def __init__(self, csoc) -> None:
        self.socket = csoc


class Player():
    def __init__(self, user) -> None:
        self.user = user
        self.socket = user.socket
        

    def ask_role(self):
        ...
        #TODO

    def ask_action(self):
        try:
            action = self.socket.recv_msg()
        except:
            pass
