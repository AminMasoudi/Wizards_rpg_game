import threading
import time 
from consts import ROLES

import random

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
        time.sleep(15)
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
            self.player2.socket.send_json({
                "type": type,
                "status" : status
            })
            print("[game inited]")

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
        p1_dead  = self.player1.role.remaining_life < 1
        p2_dead = self.player2.role.remaining_life < 1
        over = False
        if p1_dead and not p2_dead:
            self.winner = self.player2
            over = True
        elif (not p1_dead) and p2_dead:
            self.winner = self.player1
            over = True
        elif p1_dead and p2_dead:
            over = True 
            self.winner = False
                    
        return over
        #TODO
     
    def play_round(self):
        time.sleep(5)
        print("[Calculating] Calculating game result")
        p1 = self.player1
        p2 = self.player2

        p1.calc_rem_life(p2)
        p2.calc_rem_life(p1)

        p1.last_action = False
        p2.last_action = False

        p1.socket.send_json({
            "type" : "game_info",
            "content" : {
                "player" : p1.role.ser(),
                "player_b"   : p1.role.ser(),
            },
        })
        p2.socket.send_json({
            "type" : "game_info",
            "content" : {
                "player" : p2.role.ser(),
                "player_b"   : p1.role.ser(),
            },
        })



        # waite 10 sec
        # calculate rem lives
        # reset action and flags and ...
        # send them the result


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

    def ser(self):
        content = {
            "name"    : self.name,
            "re_life" : self.remaining_life,
            "magic"   : self.magic,  
        }
        return  content


class User():
    def __init__(self, csoc) -> None:
        self.socket = csoc


class Player():
    def __init__(self, socket) -> None:
        self.socket = socket
        self.role = None
        self.last_action = False
        #TODO UUID and roll asking

    def ask_role(self):
        print(f"[ask role] {self}")
        # roles = list(map(lambda x: x.serilizer(), ROLES))
        self.socket.send_json({
            "type" : "ask_role",
            "roles" : ROLES
        })

    def default_role(self):
        if not self.role:
            self.role = Role(ROLES[0])

    def calc_rem_life(self, o_player):
        # self.role.remaining_life -= 10
        # self.role.magic -= 1
        o_action = o_player.last_action
        
        if o_action == "attack":
            if self.last_action == "defend":
                #calculate
                to_effect = o_player.role.effective_hit /100
                n = 1-to_effect
                if random.choices([0,1],[n,to_effect]):
                    self.role.remaining_life -= o_player.role.power
                
            else:
                self.role.remaining_life -= o_player.role.power

        elif o_action == "magic":
            ...
        
