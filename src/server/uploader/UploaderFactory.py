from .LocalUploader import LocalUploader
from .RemoteUploader import RemoteUploader
from .AbstractUploader import AbstractUploader
from server.FileHandlerFactory import FileHandlerFactory
from utils.config import config

class UploaderFactory(object):
    
    @staticmethod
    def get_uploader(is_local: bool=True) -> AbstractUploader:
        file_handler = FileHandlerFactory.get_file_handler()
        randomize_port = config.get_randomize_port()
        if is_local:
            return LocalUploader(file_handler, randomize_port)
        else:
            return RemoteUploader(file_handler, randomize_port)
        