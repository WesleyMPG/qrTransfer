from server.FileHandlerFactory import FileHandlerFactory
from utils.config import config
from utils import get_local_network_ip
from .LocalUploader import LocalUploader
from .RemoteUploader import RemoteUploader
from .AbstractUploader import AbstractUploader
from .helpers import PortProvider


class UploaderFactory(object):
    
    @staticmethod
    def get_uploader(is_local: bool=True) -> AbstractUploader:
        file_handler = FileHandlerFactory.get_file_handler()
        if is_local:
            ip = UploaderFactory.__get_ip()
            port = UploaderFactory.__get_port()
            return LocalUploader(file_handler, ip, port)
        else:
            return RemoteUploader(file_handler)
    
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
        