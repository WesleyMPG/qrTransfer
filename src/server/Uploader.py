import requests as req
import pathlib
from server import FileHandler
from utils import get_local_network_ip, config


PORT = config['network']['PORT']


class Uploader(object):
    """A manager to upload modes.

    Args:
        mode (int, optional): Defaults to Uploader.LOCAL_MODE.
            Can also be Uploader.REMOTE_MODE.
    
    Raises:
        ValueError: If mode is unknown.
    """
    LOCAL_MODE = 0
    REMOTE_MODE = 1

    def __init__(self, mode=LOCAL_MODE):
        self.__mode = mode
        self.__path = ''
        self.__fhandler = FileHandler()
        
    def upload(self, path_list):
        """Upload a file.
        """
        path = self.__fhandler.resolve_files(path_list)
        if self.__mode == Uploader.LOCAL_MODE:
            return self.__local_upload(path)
        elif self.__mode == Uploader.REMOTE_MODE:
            return self.__remote_upload(path)
        else:
            raise Exception('Invalid mode.')  #TODO: change to ValueError

    def done(self):
        """Has things to be done after upload complete.
        """
        if self.__mode == Uploader.LOCAL_MODE:
            self.__fhandler.delete_files()

    def __local_upload(self, path):
        filename = pathlib.Path(path).name
        ip = get_local_network_ip()
        return f'http://{ip}:{PORT}/download/{filename}'

    def __remote_upload(self, path):
        """Uploads the file to file.io
        """
        with open(path, 'rb') as file:
            r = req.post(
                'https://file.io/?expires=1d',
                files={'file': file}
            )
        return r.json()['link']

    


if __name__ == "__main__":
    u = Uploader()
    #u.upload('~/Teste/sem_título.mp4')
