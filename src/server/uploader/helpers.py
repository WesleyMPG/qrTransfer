import socket
from random import randint
from utils.config import config
from utils import get_local_network_ip

class URLProvider:

    @staticmethod
    def get_url():
        ip = URLProvider.__get_ip()
        port = URLProvider.__get_port()
        return f'http://{ip}:{port}'

    @staticmethod
    def __get_ip():
        if config.get_auto_select_ip().as_bool():
            return get_local_network_ip()
        else:
            return config.get_ip()
        
    @staticmethod
    def __get_port():
        if not config.get_randomize_port().as_bool():
            return config.get_port()
        return PortProvider().get_random_port()


class PortProvider:
    MAX_PORT_TRIES = 10

    def __init__(self):
        self._sock = None

    def get_random_port(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self._get_random_port()
        self._sock.close()
        if port: return port
        raise UnableToGetAvailablePortError()

    def _get_random_port(self):
        for i in range(self.MAX_PORT_TRIES):
            port = randint(5001, 9999)
            if self._is_port_available(port): break
            port = None
        return port

    def _is_port_available(self, port):
        try:
            self._sock.connect_ex(('localhost', port))
            return True
        except socket.error:
            return False


class UnableToGetAvailablePortError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__("Could\'t find an available port.", *args, **kwargs)