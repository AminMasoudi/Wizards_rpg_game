import pygame

class Screen():
    def __init__(self, size) -> None:
        self.screen = pygame.display.set_mode(size)
        self.BG_COLOR = (100, 100, 100)
        self.medium_font = pygame.font.Font(None, 50)

        
        
    def back_ground(self):
        self. screen.fill(self.BG_COLOR)

    def draw_text(self, text, coordinate):
        color  = "White" if self.BG_COLOR != "White" else "Black"
        text = self.medium_font.render(text, True, color)
        self.screen.blit(text, coordinate)


class Index(Screen):
    pass