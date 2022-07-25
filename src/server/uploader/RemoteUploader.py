import requests as req
import logging


class RemoteUploader(object):

    def __init__(self):
        super().__init__(logging.getLogger(f'Main.{__name__}'))
            
    def _get_link(self, path_list):
        path = self.__fhandler.resolve_files(path_list)
        self.__log.debug(f'upload - Path: {path}.')
        return self.__upload_remotely(path)

    def __upload_remotely(self, path):
        with open(path, 'rb') as file:
            response = req.post(
                'https://file.io/?expires=1d',
                files={'file': file}
            )
        return response.json()['link']
