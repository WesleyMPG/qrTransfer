import pathlib, logging
from utils import get_local_network_ip, config
from .AbstractUploader import AbstractUploader


class LocalUploader(AbstractUploader):

    PORT = config['network']['PORT']

    def __init__(self, file_handler):
        super().__init__(file_handler, logging.getLogger(f'Main.{__name__}'))
        self._ip = get_local_network_ip()
            
    def _get_link(self, path_list):
        path = self._fhandler.resolve_files(path_list)
        self._log.debug(f'upload - Path: {path}.')
        if isinstance(path, str):
            return self._upload(path)
        else:
            return self._upload_no_zip(path)

    def _upload(self, path):
        filename = pathlib.Path(path).name
        return f'http://{self._ip}:{self.PORT}/download/{filename}'    

    def _upload_no_zip(self, path_list):
        return f'http://{self._ip}:{self.PORT}/download/'