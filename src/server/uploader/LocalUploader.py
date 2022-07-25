import pathlib, logging
from utils import get_local_network_ip, config
from .AbstractUploader import AbstractUploader


class LocalUploader(AbstractUploader):

    PORT = config['network']['PORT']

    def __init__(self):
        super().__init__(logging.getLogger(f'Main.{__name__}'))
            
    def _get_link(self, path_list):
        path = self.__fhandler.resolve_files(path_list)
        self.__log.debug(f'upload - Path: {path}.')
        return self.__upload_locally(path)

    def __upload_locally(self, path):
        filename = pathlib.Path(path).name
        ip = get_local_network_ip()
        return f'http://{ip}:{LocalUploader.PORT}/download/{filename}'    
