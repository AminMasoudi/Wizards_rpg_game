import os

SIZE = WIDTH, HEIGHT = 800, 450
FPS = 60
GAME_NAME="RPG"
BG_COLOR = (75, 75, 75)
FONT = None
page = "index"

def set_page(page):
    os.environ["PAGE"] = page

def get_page():
    return os.getenv("PAGE")


set_page(page)