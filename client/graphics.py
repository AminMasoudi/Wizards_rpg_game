import pygame
from consts import *


class Button:
    def __init__(self, pos, width, height, type, data) -> None:
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        if type == "role": 
            self.data = data
        elif type == "game_btn": 
            self.data=data
        else:
            self.data = None


    def is_touched(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.text_color = "#e0e0e0"
            self.bg_color   = "#101010"
            return True
        else:
            self.text_color = "Black"
            self.bg_color = "White"
            return False
        
    def clicked(self):
        cli, _, _ = pygame.mouse.get_pressed()
        if self.is_touched() and cli : 
            return True
        else:
            False

    def draw_btn(self, surf, font, text):
        self.is_touched()
        btn_text = font.render(text, True, self.text_color)
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.center = self.rect.center
        pygame.draw.rect(surf, self.bg_color, self.rect, 0, 10)
        surf.blit(btn_text, btn_text_rect)




class Screen:
    def __init__(self, size) -> None:
        self.screen = pygame.display.set_mode(size)
        self.med_font = pygame.font.Font("client/fonts/OpenSans-Regular.ttf",40)
        self.small_font = pygame.font.Font("client/fonts/OpenSans-Regular.ttf",20)
        self.large_font = pygame.font.Font("client/fonts/OpenSans-Regular.ttf",70)
        self.screen_rec = self.screen.get_rect()
        self.btn = []
        
    def draw_text_m(self, text, pos, color):
        text = self.med_font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = pos
        self.screen.blit(text, text_rect)

    def draw_text_l(self, text, pos, color):
        text = self.large_font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = pos
        self.screen.blit(text, text_rect)

    def draw_vertical_line(self, left_pos, color="White"):
        y0 = 0
        y1 = HEIGHT
        pygame.draw.line(surface    = self.screen,
                         color      = color,
                         start_pos  = (left_pos, y0),
                         end_pos    = (left_pos, y1))

    def draw_btn(self, pos, text, type="role", role=None):
        btn = Button(pos, 200, 75, type=type, data=role)
        btn.draw_btn(self.screen, self.med_font, text)
        self.btn.append(btn)


class LifeBar:
    def __init__(self, left, surf) -> None:
        self.left = left
        self.surf = surf
        self.rect = pygame.Rect(left, 120, 800, 100)
        pygame.draw.rect(surf, "White", self.rect, 2, 5)

    def draw_life(self, left, re_life):
        re_life *= 8
        life_rect = pygame.Rect(left, 120, re_life, 100)
        pygame.draw.rect(self.surf, "White", life_rect)
