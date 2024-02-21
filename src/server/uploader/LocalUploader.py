import logging
from .AbstractUploader import AbstractUploader


class LocalUploader(AbstractUploader):

    def __init__(self, file_handler, url):
        super().__init__(file_handler, logging.getLogger(f'Main.{__name__}'))
        self._url = url
            
    def _get_link(self, path_list):
        self._uploaded_files = self._fhandler.resolve_files(path_list)
        self._log.debug(f'upload - Path: {self._uploaded_files}.')
        if len(self._uploaded_files) == 1:
            return self._upload_one_file()
        else:
            return self._upload_multiple()

    def _upload_one_file(self):
        filename = self._uploaded_files[0].name
        return f'{self._url}/download/{filename}'    

    def _upload_multiple(self):
        return f'{self._url}/download/'