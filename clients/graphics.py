import pygame as pg
from connection import Client, WebServer


class Screen:
    def __init__(self, size) -> None:
        self.page           = "index"
        self.screen         = pg.display.set_mode(size)
        self.client         = Client()
        self.status         = ''
        self.er_msg         = ""
        self.text_input     = ""
        self.large_font     = pg.font.Font("clients/OpenSans-Regular.ttf", 70)
        self.screen_rect    = self.screen.get_rect()
        self.medium_font    = pg.font.Font("clients/OpenSans-Regular.ttf", 40)
        self.screen.fill("#888888")
        
    def index(self):
        input_rect = pg.Rect(1,1,800, 75)
        input_rect.center = self.screen_rect.center
        pg.draw.rect(self.screen, "White", input_rect)
        
        self.draw_text_m(self.text_input, self.screen_rect.center, "Black")
        
        if self.er_msg :
            x, _ = self.screen_rect.center
            self.draw_text_l(self.er_msg, (x, 200))
    
    def role_page(self):
        self.btn = []
        self.draw_vertical_line()
        x, _ = self.screen_rect.center
        self.draw_text_l("Choose your Role", (x//2, 120))

        for role_index in range(len(self.roles)):
            h = 2 * self.screen_rect.bottom // 6 + 100 * role_index + 20
            btn = Button((x//2, h), 200, 75, role_index)
            btn.draw_btn(
                self.screen,
                self.medium_font,
                self.roles[role_index]["name"]
            )
            self.btn.append(btn)

        for btn in self.btn:
            if btn.is_touched():
                self.explain_role_index = btn.data
            if btn.clicked() :
                if self.client.post_role_id(self.roles[role_index]["id"]):
                    game_data = self.client.get_game()
                    if game_data:
                        self.game_info = game_data
                        print(self.game_info)
                        self.game_init_api = False
                        self.page = "game"
                        self.ws_connection = False
                        
                else:
                    print("[FAILED] failed to submit the role")
                    


        #explain role
        try:
            explain_role = self.roles[self.explain_role_index]
            self.draw_text_l(explain_role["name"], (3 * x // 2, 120)) 
            self.draw_text_m(
                f"power :    {explain_role['power']}",
                (3 * x // 2, 220)
            )
            self.draw_text_m(
                f"magic :    {explain_role['magic']}",
                (3 * x // 2, 290)
            )
            self.draw_text_m(
                f"Efective Defend :    {explain_role['ef_defend']}",
                (3 * x // 2, 360)
            )
        except:
            pass

    def game_page(self):
        self.btn = []

        if not self.ws_connection:
            self.ws = WebServer(f"socket-server/{self.game_info['pk']}",self)  
            #TODO listening ws
            self.ws_connection = True


            
        if self.game_info['status'] == "started":
            self.draw_vertical_line()
            p1_center = self.screen_rect.width // 4
            p2_center = 3 * self.screen_rect.width // 4
            l1 = LifeBar(p1_center, self.screen)
            l2 = LifeBar(p2_center, self.screen)
            
            try:
                re_life_1   = self.game_info["player"]["u_player"]["role"]["re_life"]
                p_role_name = self.game_info["player"]["u_player"]["role"]["name"]
                p_magic     = self.game_info["player"]["u_player"]["role"]["magic"]

                re_life_2   = self.game_info["player"]["o_player"]["role"]["re_life"]
                p2_role_name= self.game_info["player"]["o_player"]["role"]["name"]
                p2_magic    = self.game_info["player"]["o_player"]["role"]["magic"]


            except:
                re_life_1    = 0
                re_life_2    = 0

                p_role_name  = "FOO"
                p2_role_name = "BAR"

                p_magic     = 0
                p2_magic    = 0



            l2_left = l2.rect.left  + (100-re_life_2) * 8
            l1.draw_life(l1.rect.left, re_life_1)
            l2.draw_life(l2_left, re_life_2)
            
            #name
            self.draw_text_l(f"NAME : {p_role_name}", (p1_center, 300))
            self.draw_text_l(f"NAME : {p2_role_name}", (p2_center, 300))
            #re_life
            self.draw_text_m(f"Remaining life : {re_life_1}",(p1_center, 365))
            self.draw_text_m(f"Remaining life : {re_life_2}",(p2_center, 365))
            #magic
            self.draw_text_m(f"Magics : {p_magic}", (p1_center, 420))
            self.draw_text_m(f"Magics : {p2_magic}", (p2_center, 420))
            
            #btn
            #defend
            defend_btn = Button((180, 1080), 200, 75, "defend")
            defend_btn.draw_btn(self.screen, self.medium_font, "Defend")
            self.btn.append(defend_btn)
            #attack
            attack = Button((480,1080), 200, 75, "attack")
            attack.draw_btn(self.screen, self.medium_font, "Attack")
            self.btn.append(attack)

            magic = Button((780, 1080), 200, 75, "magic")
            magic.draw_btn(self.screen, self.medium_font, "Magic")
            self.btn.append(magic)

            for btn in self.btn:
                if btn.clicked():
                    self.ws.submit_action(btn.data)
        
            

        else:
            self.draw_text_l(f"STATUS : {self.game_info['status']}", self.screen_rect.center)
        
    
    def event_handler(self):

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                self.run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]

                elif event.key == pg.K_RETURN:
                    self.submit()

                elif len(self.text_input) < 15:

                    self.text_input += event.unicode


    def draw_text_m(self, text, center_pos, color="White"):
        text = self.medium_font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = center_pos
        self.screen.blit(text, text_rect)

    def draw_text_l(self, text, center_pos, color="White"):

        text = self.large_font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = center_pos
        self.screen.blit(text, text_rect)        

    def draw_vertical_line(self):
        y1 = self.screen.get_size()[1]
        x  = self.screen.get_size()[0] //2 
        pg.draw.line(
            self.screen,
            "White",
            (x, 0),
            (x, y1)
        )

    def submit(self):
        if self.page == "index":
            # auth , self.csrf = post_auth(self.text_input)
            auth = self.client.post_auth(self.text_input)
            if auth :
                if auth["result"] == "ok":
                    self.page = "roles"
                    self.get_roles = False
                    self.submited_role = False
                else: 
                    print("[FAILED] : failed to auth")
                    self.er_msg = "Failed to authenticate"

class Button:
    def __init__(self, center, width, height, data) -> None:                                                        
        self.rect = pg.Rect(center[0], center[1], width, height)  
        self.rect.center = center                                                       
        self.data = data

    def draw_btn(self, surf, font, text):
        self.is_touched()
        btn_text = font.render(text, True, self.text_color)
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = self.rect.center
        pg.draw.rect(surf, self.bg_color, self.rect, 0, 10)
        surf.blit(btn_text, btn_text_rect)

    def is_touched(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.text_color = "#e0e0e0"
            self.bg_color   = "#101010"
            return True
        else:
            self.text_color = "Black"
            self.bg_color = "White"
            return False

    def clicked(self):
        cl, _, _ = pg.mouse.get_pressed()
        if self.is_touched() and cl:
            return True
        return False
    
class LifeBar:
    def __init__(self, center_x_pos, surf) -> None:
        self.surf = surf
        self.rect = pg.Rect(100, 120, 800, 100)
        self.rect.center = (center_x_pos, 170)
        pg.draw.rect(surf, "white", self.rect, 2, 5)

    def draw_life(self, left, re_life):
        re_life *= 8
        life_rect = pg.Rect(left, 120, re_life, 100)
        pg.draw.rect(self.surf, "White", life_rect)