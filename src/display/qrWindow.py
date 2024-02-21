import os
os.environ['KIVY_NO_ARGS'] = '1'
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from PIL import Image
from utils import ROOT_DIR
from .helper import pillImg_to_texture
from .settings_screen import SettingsScreen


Window.size = (400, 500)
DISPLAY_DIR = ROOT_DIR.joinpath('display')
kv_file = DISPLAY_DIR.joinpath('kvFiles', 'qrWindow.kv')

Builder.load_file(str(kv_file))

#TODO: criar a configuração de escolher ip

class QrFrameScreen(Screen):
    """Container for the qrCode image
    """
    def __init__(self, code, **kwargs):
        super(QrFrameScreen, self).__init__(**kwargs)
        self.ids.txt.text = "DON'T close this window\n"+ \
                            "until download complete"
        self.ids.img.texture = pillImg_to_texture(code)


class QrApp(MDApp):
    def __init__(self, code, **kwargs):
        super(QrApp, self).__init__(**kwargs)
        self._code = code
        self._sm = ScreenManager()
        self.title = 'QrTransfer'
        

    def build(self):
        Window.clearcolor = (.1, .1, .1, 1)
        self.__setup_icon()
        self.__add_screens()
        return self._sm
    
    def __setup_icon(self):
        p = ROOT_DIR.joinpath('resources', 'icon.png')
        self.icon = str(p)

    def __add_screens(self):
        self._sm.add_widget(QrFrameScreen(self._code, name='qrframe'))
        self._sm.add_widget(SettingsScreen(name='settings'))


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
