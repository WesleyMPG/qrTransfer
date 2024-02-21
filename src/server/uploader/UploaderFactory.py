from server.FileHandlerFactory import FileHandlerFactory
from utils.config import config
from utils import get_local_network_ip
from .LocalUploader import LocalUploader
from .RemoteUploader import RemoteUploader
from .AbstractUploader import AbstractUploader
from .helpers import URLProvider

class UploaderFactory(object):
    
    @staticmethod
    def get_uploader(is_local: bool=True) -> AbstractUploader:
        file_handler = FileHandlerFactory.get_file_handler()
        if is_local:
            return LocalUploader(file_handler, URLProvider.get_url())
        else:
            return RemoteUploader(file_handler)
    
    
        