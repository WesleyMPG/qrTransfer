import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import qrcode as qr
import requests as req
from cli import file_path


def qr_gen(text):
    """Creates the qrcode image
    """
    return qr.make(text).convert('RGB')


def upload_file(path):
    """Uploads the file to file.io
    """
    with open(path, 'rb') as file:
        r = req.post(
            'https://file.io/?expires=1d',
            files={'file': file}
        )
    return r.json()['link']


def _pillImg_to_surface(img):
    """Converts the qrcode image to a pygame.Surface
    """
    mode = img.mode
    size = img.size
    data = img.tobytes()
    return pg.image.fromstring(data, size, mode)


W, H = 400, 400
def window(img):
    """Sets up the window
    """
    pg.init()
#    logo = pg.image.load('logo.png')
#    pg.display.set_icon(logo)
    pg.display.set_caption('qrTransfer')

    screen = pg.display.set_mode((W, H))

    surface = _pillImg_to_surface(img)
    rect = surface.get_rect()
    rect.center = (W//2, H//2)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.blit(surface, rect)
        pg.display.update()


def main():
    link = upload_file(file_path)
    print('Uploading file...')
    code = qr_gen(link)
    window(code)


if __name__ == "__main__":
    main()
