import os
os.environ['KIVY_NO_ARGS'] = '1'
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from io import BytesIO
from utils import ROOT_DIR, config
from PIL import Image

from .menu_items import settings_items


Window.size = (400, 500)
DISPLAY_DIR = ROOT_DIR.joinpath('display')
kv_file = DISPLAY_DIR.joinpath('kvFiles', 'qrWindow.kv')

Builder.load_file(str(kv_file))

def pillImg_to_texture(img):
    """Converts a PIL.Image into a kivy texture
    """
    img = img.resize((400, 400))
    data = BytesIO()
    img.save(data, format='png')
    data.seek(0)
    kimg_data = BytesIO(data.read())
    return CoreImage(kimg_data, ext='png').texture


class QrFrame(Widget):
    """Container for the qrCode image
    """
    def __init__(self, code, **kwargs):
        super(QrFrame, self).__init__(**kwargs)
        self.ids.txt.text = "DON'T close this window\n"+ \
                            "until download complete"
        self.ids.img.texture = pillImg_to_texture(code)


class RightContentCls(IRightBodyTouch, MDBoxLayout):
    pass


class ListCheckBoxItem(OneLineAvatarIconListItem):
    left_icon = StringProperty()
    active = BooleanProperty(config.getboolean('saving', 'ZIP_FILES'))
        
    def on_toggle(self, instance, value):
        self.active = not self.active
        config.set('saving', 'ZIP_FILES', str(self.active))


class QrApp(MDApp):
    def __init__(self, code, **kwargs):
        super(QrApp, self).__init__(**kwargs)
        self._code = code
        self.qrFrame = QrFrame(self._code)
        self.menu = MDDropdownMenu(caller=self.qrFrame.ids.config_btn, items=settings_items, width_mult=4,)


    def build(self):
        Window.clearcolor = (.1, .1, .1, 1)
        p = ROOT_DIR.joinpath('resources', 'icon.png')
        self.icon = str(p)
        return self.qrFrame


def qr_window(code, at_close=None):
    """Displays the qrCode window

    Args:
        code (PILL.Image): the qrCode to be displayed
        at_close (function, optional): A function to be executed
            after window close. Defaults to None.
    """
    QrApp(code).run()
    if at_close: at_close()


if __name__ == '__main__':
    img = Image.open('../resources/icon.png')
    qr_window(img)
