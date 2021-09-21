import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from utils import resource_path

W, H = 400, 450


def _pillImg_to_surface(img):
    """Converts the qrcode image to a pygame.Surface
    """
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pg.image.fromstring(data, size, mode)


def display_line(text):
    """Displays the "don't close" message.
    """
    font_path = resource_path(
        os.path.join('resources', 'NotoSans-Regular.ttf'))
    font = pg.font.Font(font_path, 25)
    t = font.render(text, True, (255,255,255))
    rect = t.get_rect()
    return t, rect

def display_text(text):
    out = []
    for i in range(1, len(text)+1):
        t, rect = display_line(text[i-1])
        rect.center = (W//2, i*20)
        out.append((t, rect))
    return out


def display_code(img):
    """Displays the code image.
    """
    surface = _pillImg_to_surface(img)
    rect = surface.get_rect()
    rect.center = (W//2, 250)
    return surface, rect


def window(img, at_close=None):
    """Sets up the window.
    """
    pg.init()
    screen = pg.display.set_mode((W, H))
    pg.display.set_caption('qrTransfer')
#    logo = pg.image.load('logo.png')
#    pg.display.set_icon(logo)

    text = display_text(["DON'T close this window",
                         " until download complete"])
    code = display_code(img)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                if at_close: at_close()
        for t in text:
            screen.blit(*t)
        screen.blit(*code)
        pg.display.update()

