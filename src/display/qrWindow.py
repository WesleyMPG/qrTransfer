import os
os.environ['KIVY_NO_ARGS'] = '1'
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from PIL import Image
from utils import ROOT_DIR, config, ConfigName, config_handler
from .helper import pillImg_to_texture


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = {}
        self.load_config()

    def load_config(self):
        self.__load_config_on_state()
        self.__load_state_on_ui()

    def __load_config_on_state(self):
        self._state['zip?'] = config.getboolean(ConfigName.SAVING, ConfigName.ZIP_FILES)
        self._state['random_port?'] = config.getboolean(ConfigName.NETWORK, ConfigName.RANDOM_PORT)
        self._state['port'] = config.get(ConfigName.NETWORK, ConfigName.PORT)

    def __load_state_on_ui(self):
        self.ids.zip.active = self._state['zip?']
        self.ids.random_port.active = self._state['random_port?']
        self.ids.port.text = self._state['port']

    def on_toggle_zip(self, value):
        self._state['zip?'] = value
    
    def on_toggle_random_port(self, value):
        self._state['random_port?'] = value
        self.ids.port.disabled = value

    def update_port_state(self, port_input, focus_value):
        if not focus_value:
            self._state['port'] = port_input.text

    def on_save(self):
        self.__write_state_on_config()
        config_handler.save_config()
        self.go_back()

    def __write_state_on_config(self):
        config.set(ConfigName.SAVING, ConfigName.ZIP_FILES, str(self._state['zip?']))
        config.set(ConfigName.NETWORK, ConfigName.RANDOM_PORT, str(self._state['random_port?']))
        config.set(ConfigName.NETWORK, ConfigName.PORT, str(self._state['port']))

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'qrframe'


class PortInput(TextInput):
    def on_text_change(self, value: str):
        if len(value) > 5:
            self.text = value[:5]


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
