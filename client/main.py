import pygame
from client import *
from models import Screen
import threading
import time
from consts import *



connection = server_connection()


def main():
    # connection = server_connection()
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(GAME_NAME)
    clock = pygame.time.Clock()
    medium_font = pygame.font.Font(FONT, 40)
    large_font = pygame.font.Font(FONT, 70)
    global connection


    run = True
    while run:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
                connection.close()

        if get_page() == "index":
            
            # write game name
            text = large_font.render(GAME_NAME, True, "White")
            text_rect = text.get_rect()
            text_rect.center = (WIDTH//2, HEIGHT//5)
            screen.blit(text, text_rect)
             
            # game status
            game_stat = medium_font.render(connection.status, True, "White")
            gamne_stat_rect = game_stat.get_rect()
            gamne_stat_rect.center = (WIDTH//2, HEIGHT//2)
            screen.blit(game_stat, gamne_stat_rect)



        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


    
if __name__ == "__main__":
    threading.Thread(target=main).start()
    time.sleep(0.5)
    connection.status = "Seeking for Game ..."
    join_to_room(connection)

    