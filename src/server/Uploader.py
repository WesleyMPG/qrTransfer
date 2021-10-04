import requests as req
import pathlib, os
from shutil import copy2
from utils import get_local_network_ip, config


STATIC_FOLDER = config['directories']['STATIC_FOLDER']
PORT = config['network']['PORT']


class Uploader(object):
    LOCAL_MODE = 0
    REMOTE_MODE = 1

    def __init__(self, mode=LOCAL_MODE):
        self.__mode = mode
        self.__path = ''
        if mode == Uploader.LOCAL_MODE:
            self._upload = self.__local_upload
        elif mode == Uploader.REMOTE_MODE:
            self._upload = self.__remote_upload
        else:
            raise Exception('Invalid mode.')

    def upload(self, path):
        """Upload a file
        """
        return self._upload(path)

    def done(self):
        if self.__mode == Uploader.LOCAL_MODE:
            os.remove(self.__path)

    def __local_upload(self, path):
        self.__copy_file(pathlib.Path(path))
        filename = pathlib.Path(path).name
        ip = get_local_network_ip()
        return f'http://{ip}:5000/download/{filename}'

    def __remote_upload(self, path):
        """Uploads the file to file.io
        """
        with open(path, 'rb') as file:
            r = req.post(
                'https://file.io/?expires=1d',
                files={'file': file}
            )
        return r.json()['link']

    def __copy_file(self, path : pathlib.Path):
        destination = STATIC_FOLDER
        copy2(path, destination)

        self.__path = pathlib.PurePath(destination, path.name)


if __name__ == "__main__":
    u = Uploader()
    #u.upload('~/Teste/sem_título.mp4')
