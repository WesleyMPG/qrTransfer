from .LocalUploader import LocalUploader
from .RemoteUploader import RemoteUploader
from .AbstractUploader import AbstractUploader


class UploaderFactory(object):
    
    @staticmethod
    def getUploader(is_local: bool) -> AbstractUploader:
        if is_local:
            return LocalUploader
        else:
            return RemoteUploader
        