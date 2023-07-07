from connection import  get_roles, WebServer
from graphics import Screen
import pygame as pg


SIZE = WIDTH, HEIGHT = 1920, 1200
BG_COLOR = "#888888"
FPS = 30





def main():
    pg.init()
    screen = Screen(SIZE)
    pg.display.set_caption("WIZARDS WARS")
    clock = pg.time.Clock()
    
    

    screen.run = True
    while screen.run:
        # Background

        screen.screen.fill(BG_COLOR)

        screen.event_handler()


        if screen.page == "index":
            screen.index()

        if screen.page == "roles":
            if not screen.get_roles:
                roles = get_roles()
                screen.get_roles = True
                screen.roles = roles
            screen.role_page()

        if screen.page == "game":
            screen.game_page()            
             

        pg.display.update()
        clock.tick(FPS)

    pg.quit()
if __name__ == "__main__":
    main()