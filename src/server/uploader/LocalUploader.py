import pathlib, logging
from utils import get_local_network_ip, config
from .AbstractUploader import AbstractUploader


class LocalUploader(AbstractUploader):

    PORT = config.get('network', 'PORT')

    def __init__(self, file_handler):
        super().__init__(file_handler, logging.getLogger(f'Main.{__name__}'))
        self._ip = get_local_network_ip()
            
    def _get_link(self, path_list):
        handled_path_list = self._fhandler.resolve_files(path_list)
        self._log.debug(f'upload - Path: {handled_path_list}.')
        if len(handled_path_list) == 1:
            return self._upload_one_file(handled_path_list[0])
        else:
            return self._upload_multiple(handled_path_list)

    def _upload_one_file(self, path):
        filename = pathlib.Path(path).name
        return f'http://{self._ip}:{self.PORT}/download/{filename}'    

    def _upload_multiple(self, path_list):
        return f'http://{self._ip}:{self.PORT}/download/'