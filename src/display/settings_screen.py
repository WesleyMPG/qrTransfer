from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from utils.config import config, config_handler
from utils import get_ip_list


class SettingsScreen(Screen):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = {}
        self.load_config()

    def load_config(self):
        self.__load_config_on_state()
        self.__load_state_on_ui()

    def __load_config_on_state(self):
        self._state['zip?'] = config.get_zip_files().as_bool()
        self._state['randomize_port?'] = config.get_randomize_port().as_bool()
        self._state['port'] = config.get_port()
        self._state['ip'] = config.get_ip()
        self._state['auto_select_ip?'] = config.get_auto_select_ip().as_bool()

    def __load_state_on_ui(self):
        self.ids.zip.active = self._state['zip?']
        self.ids.randomize_port.active = self._state['randomize_port?']
        self.ids.port.text = self._state['port']
        self.ids.ip_selector.text = self._state['ip']
        self.ids.auto_ip.active = self._state['auto_select_ip?']

    def on_toggle_zip(self, value):
        self._state['zip?'] = value
    
    def on_toggle_randomize_port(self, value):
        self._state['randomize_port?'] = value
        self.ids.port.disabled = value
    
    def on_toggle_auto_select_ip(self, value):
        self._state['auto_select_ip?'] = value
        self.ids.ip_selector.disabled = value

    def ip_selected(self, value):
        self._state['ip'] = value

    def update_port_state(self, port_input, focus_value):
        if not focus_value:
            self._state['port'] = port_input.text

    def on_save(self):
        self.__write_state_on_config()
        config_handler.save_config()
        self.go_back()

    def __write_state_on_config(self):
        config.set_zip_files(str(self._state['zip?']))
        config.set_randomize_port( str(self._state['randomize_port?']))
        config.set_port(self._state['port'])
        config.set_ip(self._state['ip'])
        config.set_auto_select_ip(str(self._state['auto_select_ip?']))

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'qrframe'


class PortInput(TextInput):
    def on_text_change(self, value: str):
        if len(value) > 5:
            self.text = value[:5]


class IPList(Spinner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values = get_ip_list()
