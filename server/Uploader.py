import requests as req
import pathlib, os, subprocess


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
            os.system(f'rm {self.__path}')

    def __local_upload(self, path):
        self.__copy_file(pathlib.Path(path))
        filename = pathlib.Path(path).name
        ip = self.__get_local_network_ip()
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
        this_file_dir = pathlib.Path(__file__).parent.resolve()
        destination = pathlib.PurePath(this_file_dir, 'static')
        os.system(f'cp {path} {destination}')

        self.__path = pathlib.PurePath(destination, path.name)

    @staticmethod
    def __get_local_network_ip():
        sub = subprocess.Popen(
            "hostname -I | awk '{print $1}'",
            shell=True, stdout=subprocess.PIPE)
        ip = sub.stdout.read()[:-1].decode()
        return ip


if __name__ == "__main__":
    u = Uploader()
    #u.upload('~/Teste/sem_título.mp4')
