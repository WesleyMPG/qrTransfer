import logging
from utils import get_local_network_ip, config_obj, ConfigName
from .AbstractUploader import AbstractUploader
from .helpers import PortProvider


class LocalUploader(AbstractUploader):

    def __init__(self, file_handler, randomize_port=False):
        super().__init__(file_handler, randomize_port, logging.getLogger(f'Main.{__name__}'))
        self._ip = get_local_network_ip()
        self._port = self._get_port()

    def _get_port(self):
        if not self._randomize_port:
            return config_obj.get(ConfigName.NETWORK, ConfigName.PORT)
        return PortProvider().get_random_port()
            
    def _get_link(self, path_list):
        self._uploaded_files = self._fhandler.resolve_files(path_list)
        self._log.debug(f'upload - Path: {self._uploaded_files}.')
        if len(self._uploaded_files) == 1:
            return self._upload_one_file()
        else:
            return self._upload_multiple()

    def _upload_one_file(self):
        filename = self._uploaded_files[0].name
        return f'http://{self._ip}:{self._port}/download/{filename}'    

    def _upload_multiple(self):
        return f'http://{self._ip}:{self._port}/download/'