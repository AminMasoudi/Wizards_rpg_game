import threading
import time 
ROLES = []


class Game():
    
    def __init__(self) -> None:
        self.inited = False
        self.pending = True
        self.player1 = None
        self.player2 = None

    def init_game(self):
        print(self.player1, self.player2)
        self.player1.ask_role()
        self.player2.ask_role()
        time.sleep(10)
        self.player1.default_role()
        self.player2.default_role()

        self.broadcast("game_inited", "new_status")
        self.inited = True


    def broadcast(self, status, type, ):
        try:
            self.player1.socket.send_json({
                "type": type,
                "status" : status
            })
            self.player1.socket.send_json({
                "type": type,
                "status" : status
            })

        except:
        
            return False




    def start(self):
        self.init_game()
        print("inited")
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
        threading.Thread(target=self.player2.ask_action()).start()
        threading.Thread(target=self.player1.ask_action()).start()

        # - [ ] 

    #player 2
    #  



class Role():
    def __init__(self,role_dict) -> None:
        self.role_dict = role_dict
        self.name   = role_dict["name"]
        self.magic  = role_dict["magic"]
        self.power  = role_dict["power"]


        self.remaining_life      = 100
        self.effective_defend    = role_dict["e_defend"]
        self.effective_hit       = role_dict["e_hit"]
        self.effective_magic     = role_dict["e_magic"]
        self.magic_recovery_rate = role_dict["MRR"]

    def serilizer(self):
        return self.role_dict


class User():
    def __init__(self, csoc) -> None:
        self.socket = csoc


class Player():
    def __init__(self, socket) -> None:
        self.socket = socket
        self.role = None
        #TODO UUID and roll asking

    def ask_role(self):
        print(f"[ask role] {self}")
        roles = list(map(lambda x: x.serilizer(), ROLES))
        self.socket.send_json({
            "type" : "ask_role",
            "roles" : roles
        })

    def default_role(self):
        if not self.role:
            self.role = ROLES[0]

    def ask_action(self):
        try:
            action = self.socket.recv_msg()
        except:
            pass
