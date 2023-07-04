import pygame
from client import *
# from models import Screen
from graphics import Screen, Button, LifeBar
import threading
import time
from consts import *



connection = server_connection()





def main():
    # connection = server_connection()
    pygame.init()
    screen = Screen(SIZE)
    pygame.display.set_caption(GAME_NAME)
    clock = pygame.time.Clock()
    global connection



    run = True
    while run:
        screen.screen.fill(BG_COLOR)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

        page = get_page()
        if page == "index":
            
            # Game name
            screen.draw_text_l(text=GAME_NAME,
                               pos=(WIDTH//2, HEIGHT//5),
                               color="White" 
                                )
            # game status
            screen.draw_text_m(text=connection.status,
                               pos=screen.screen_rec.center,
                               color="White")

        elif page == "ask_role":
            screen.btn = []
            
            screen.draw_text_m("Chose your Role",
                               (WIDTH//4, HEIGHT//6),
                               color= "White")
            
            # midel line
            midel_x, _ = screen.screen_rec.center
            screen.draw_vertical_line(midel_x)
            # btn

            for role in range(len(connection.roles)):
                top = ((2*HEIGHT)//6 + role*100 + 20)
                screen.draw_btn((75, top), connection.roles[role]["name"], role=connection.roles[role])

            for btn in screen.btn:
                if btn.clicked() and not connection.sended:
                    submit_role(connection, btn.data)
                    print("submit")
        
        elif page ==     "game":
            screen.btn = []

            midel_x , _ = screen.screen_rec.center 
            screen.draw_vertical_line(midel_x)
            
            # life bar 1

            l = LifeBar(100, screen.screen)
            try:
                re_life = connection.game_data["player"]["re_life"]
                re_life_2 = connection.game_data["player_b"]["re_life"]
            except:
                re_life = 0
                re_life_2 = 0

            l.draw_life(l.left, re_life)
            
            # life bar 2
            l2 = LifeBar(1020, screen.screen)
            l2_rect = pygame.Rect(1820 - re_life_2*8, 120, re_life_2*8, 100)
            pygame.draw.rect(screen.screen, "White", l2_rect)
            # player 1 info
            try:
                # name
                name_text = screen.large_font.render(f"NAME :    {connection.game_data['player']['name']}", True, "White")
                name_text_rect = name_text.get_rect()
                name_text_rect.top = 270
                name_text_rect.left = 100
                screen.screen.blit(name_text, name_text_rect)
                # Life
                life_text = screen.med_font.render(f"Remaining life:    {re_life}", True, "White")
                life_text_rect = life_text.get_rect()
                life_text_rect.top = 370
                life_text_rect.left = 100
                screen.screen.blit(life_text, life_text_rect)
                #magic
                magic_text = screen.med_font.render(f"Magic :   {connection.game_data['player']['magic']}", True, "White")
                magic_text_rect = magic_text.get_rect()
                magic_text_rect.top = 440
                magic_text_rect.left = 100
                screen.screen.blit(magic_text, magic_text_rect)

                # player 2 info
                # name
                name2_text = screen.large_font.render(f"NAME :    {connection.game_data['player_b']['name']}", True, "White")
                name2_text_rect = name2_text.get_rect()
                name2_text_rect.top = 270
                name2_text_rect.left = 1020
                screen.screen.blit(name2_text, name2_text_rect)
                #player 2 life
                life2_text = screen.med_font.render(f"Remaining life:    {re_life_2}", True, "White")
                life2_text_rect = life2_text.get_rect()
                life2_text_rect.top = 370
                life2_text_rect.left = 1020
                screen.screen.blit(life2_text, life2_text_rect)
                #player 2 magic
                magic2_text = screen.med_font.render(f"Magic :   {connection.game_data['player_b']['magic']}", True, "White")
                magic2_text_rect = magic2_text.get_rect()
                magic2_text_rect.top = 440
                magic2_text_rect.left = 1020
                screen.screen.blit(magic2_text, magic2_text_rect)

                # defend button 
                defend_btn = Button((100, 1080), 200, 75, "game_btn", "defend")
                defend_btn.draw_btn(screen.screen, screen.med_font, "Defend")
                screen.btn.append(defend_btn)
                # magic btn
                magic_btn = Button((400, 1080), 200, 75, "game_btn", "magic")
                magic_btn.draw_btn(screen.screen, screen.med_font, "Magic")
                screen.btn.append(magic_btn)
                # attack btn
                attack_btn = Button((700, 1080), 200, 75, "game_btn", "attack")
                attack_btn.draw_btn(screen.screen, screen.med_font, "Attack")
                screen.btn.append(attack_btn)

            except:
                pass




            for btn in screen.btn:
                if btn.clicked() and not connection.send_action : 
                    submit_action(connection, btn.data)




        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    connection.close()


    
if __name__ == "__main__":
    set_page("index")
    threading.Thread(target=main).start()
    time.sleep(0.5)
    connection.status = "Seeking for Game ..."
    join_to_room(connection)

    