import os

SIZE = WIDTH, HEIGHT = 1920, 1200
FPS = 60
GAME_NAME="RPG"
BG_COLOR = "#888888"
FONT = None


def set_page(page):
    os.environ["PAGE"] = page

def get_page():
    return os.getenv("PAGE")

