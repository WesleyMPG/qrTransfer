import requests as req
import logging
from .AbstractUploader import AbstractUploader

class RemoteUploader(AbstractUploader):

    def __init__(self, file_handler):
        super().__init__(file_handler, logging.getLogger(f'Main.{__name__}'))
            
    def _get_link(self, path_list):
        path = self.__fhandler.resolve_files(path_list)
        self._log.debug(f'upload - Path: {path}.')
        return self._upload_remotely(path)

    def __upload_remotely(self, path):
        with open(path, 'rb') as file:
            response = req.post(
                'https://file.io/?expires=1d',
                files={'file': file}
            )
        return response.json()['link']
