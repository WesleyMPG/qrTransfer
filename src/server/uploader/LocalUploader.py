import pathlib, logging
from utils import get_local_network_ip, config
from .AbstractUploader import AbstractUploader


class LocalUploader(AbstractUploader):

    PORT = config.get('network', 'PORT')

    def __init__(self, file_handler):
        super().__init__(file_handler, logging.getLogger(f'Main.{__name__}'))
        self._ip = get_local_network_ip()
        self._uploaded_files = []
            
    def _get_link(self, path_list):
        self._uploaded_files = self._fhandler.resolve_files(path_list)
        self._log.debug(f'upload - Path: {self._uploaded_files}.')
        if len(self._uploaded_files) == 1:
            return self._upload_one_file()
        else:
            return self._upload_multiple()

    def _upload_one_file(self):
        filename = self._uploaded_files[0].name
        return f'http://{self._ip}:{self.PORT}/download/{filename}'    

    def _upload_multiple(self):
        return f'http://{self._ip}:{self.PORT}/download/'