import os
os.environ['KIVY_NO_ARGS'] = '1'
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty
from kivymd.uix.list import OneLineAvatarIconListItem
from PIL import Image
from utils import ROOT_DIR, config, ConfigName
from .helper import pillImg_to_texture
from .menu_items import settings_items


Window.size = (400, 500)
DISPLAY_DIR = ROOT_DIR.joinpath('display')
kv_file = DISPLAY_DIR.joinpath('kvFiles', 'qrWindow.kv')

Builder.load_file(str(kv_file))


class QrFrameScreen(Screen):
    """Container for the qrCode image
    """
    def __init__(self, code, **kwargs):
        super(QrFrameScreen, self).__init__(**kwargs)
        self.ids.txt.text = "DON'T close this window\n"+ \
                            "until download complete"
        self.ids.img.texture = pillImg_to_texture(code)


class SettingsScreen(Screen):
    pass


class SettingsMenuCheckBoxItem(OneLineAvatarIconListItem):
    name = StringProperty()
    left_icon = StringProperty()
    active = BooleanProperty(config.getboolean(ConfigName.SAVING, ConfigName.ZIP_FILES))
        
    def on_toggle(self, instance, value):
        self.active = not self.active
        config.set(ConfigName.SAVING, ConfigName.ZIP_FILES, str(self.active))


class QrApp(MDApp):
    def __init__(self, code, **kwargs):
        super(QrApp, self).__init__(**kwargs)
        self._code = code
        self._sm = ScreenManager()
        

    def build(self):
        Window.clearcolor = (.1, .1, .1, 1)
        self.__setup_icon()
        self.__add_screens()
        return self._sm
    
    def __setup_icon(self):
        p = ROOT_DIR.joinpath('resources', 'icon.png')
        self.icon = str(p)

    def __add_screens(self):
        self._sm.add_widget(SettingsScreen(name='settings'))
        self._sm.add_widget(QrFrameScreen(self._code, name='qrframe'))


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
