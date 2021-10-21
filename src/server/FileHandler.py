import os.path as osp, logging
from os import replace, walk as os_walk, remove
from zipfile import ZipFile
from shutil import copy2
from werkzeug.utils import secure_filename
from utils import config


log = logging.getLogger(f'Main.{__name__}')

STATIC_FOLDER = config['directories']['STATIC_FOLDER']

class FileHandler(object):

    def __init__(self, out_dir=STATIC_FOLDER):
        self._out_dir = out_dir
        self._zip_out = osp.join(out_dir, 'qrTransfer-files.zip')
        self._deletion_list = []

    def __copy_file(self, path):
        """Copy one file to STATIC_FOLDER.

        Copy one file and adds its path to _deletion_list
        """
        file_name = secure_filename(osp.basename(path))
        file_path = osp.join(self._out_dir, file_name)
        copy2(path, file_path)
        log.debug(f'copy - {path} copied to {file_path}.')
        self._deletion_list.append(file_path)
        return file_path
    
    def __zip_dir(self, path, zip_file):
        len_path = len(osp.dirname(path))+1
        for folder, subfolders, filenames in os_walk(path):
            for name in filenames:
                file_path = osp.join(folder, name)
                relative_path = file_path[len_path:]
                zip_file.write(file_path, relative_path)

    def _gen_zip(self, path_list):
        with ZipFile(self._zip_out, 'w') as z:
            for path in path_list:
                log.debug(f'zip - {path}.')
                len_path = len(osp.dirname(path))+1
                if osp.isdir(path):
                    self.__zip_dir(path, z)
                else:
                    z.write(path, path[len_path:])
        self._deletion_list.append(self._zip_out)
        return self._zip_out

    def resolve_files(self, path_list):
        """Generate a single path for the path_list.

        If path_list contains only one path which is a directory or
        multiple paths a .zip is file created else a copy of the file
        is generated.

        Returns:
            str: path to file.
        """
        if len(path_list) == 1 \
        and not osp.isdir(path_list[0]):
            return self.__copy_file(path_list[0])
        else:
            return self._gen_zip(path_list)

    def delete_files(self):
        """Delete all files copied or created.
        """
        for f in self._deletion_list:
            log.debug(f'delete - {f}.')
            remove(f)


if __name__ == '__main__':
    paths = ['/home/wesley/coding/python/qrTransfer/src/scripts',
        '/home/wesley/coding/python/qrTransfer/src/cli.py',
        '/home/wesley/coding/python/qrTransfer/src/config.ini',
        '/home/wesley/coding/python/qrTransfer/src/resources',
        '/home/wesley/coding/python/qrTransfer/src/main.py',
        '/home/wesley/coding/python/qrTransfer/src/utils.py',
        ]
    #print(osp.basename(paths[0]))
    f = FileHandler()
    print(f.resolve_files(paths))
