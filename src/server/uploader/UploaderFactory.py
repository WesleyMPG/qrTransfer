from .LocalUploader import LocalUploader
from .RemoteUploader import RemoteUploader
from .AbstractUploader import AbstractUploader
from src.server.FileHandlerFactory import FileHandlerFactory


class UploaderFactory(object):
    
    @staticmethod
    def getUploader(is_local: bool) -> AbstractUploader:
        file_handler = FileHandlerFactory.get_file_handler()
        if is_local:
            return LocalUploader(file_handler)
        else:
            return RemoteUploader(file_handler)
        