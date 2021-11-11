import os.path as osp, logging
from os import replace, walk as os_walk, remove
from pathlib import Path
from zipfile import ZipFile
from shutil import copy2
from werkzeug.utils import secure_filename
from utils import config


log = logging.getLogger(f'Main.{__name__}')

STATIC_FOLDER = Path(config['directories']['STATIC_FOLDER'])

class FileHandler(object):

    def __init__(self):
        self._out_dir = STATIC_FOLDER
        self._zip_out = STATIC_FOLDER.joinpath('qrTransfer-files.zip')
        self._deletion_list = []

    def __copy_file(self, path):
        """Makes a copy to STATIC_FOLDER.

        It copies the file and adds its path to _deletion_list
        
        Args:
            path (pathlib.Path)
        """
        file_name = secure_filename(path.name)
        file_path = self._out_dir.joinpath(file_name)
        copy2(path, file_path)
        log.debug(f'copy - {path} copied to {file_path}.')
        self._deletion_list.append(file_path)
        return file_path
    
    def __zip_dir(self, path, zip_file):
        """This adds a folder to 'zip_file'

        Args:
            path (str)
            zip_file (zipfile.ZipFile)
        """
        len_path = len(osp.dirname(path))+1
        for folder, subfolders, filenames in os_walk(path):
            for name in filenames:
                file_path = osp.join(folder, name)
                relative_path = file_path[len_path:]
                zip_file.write(file_path, relative_path)

    def _gen_zip(self, path_list):
        """Generates a zip file.

        Args:
            path_list (list of pathlib.Path)
        """
        with ZipFile(self._zip_out, 'w') as z:
            for path in path_list:
                log.debug(f'zip - {path}.')
                if path.is_dir():
                    self.__zip_dir(str(path), z)
                else:
                    z.write(path, path.name)
        self._deletion_list.append(self._zip_out)
        return self._zip_out

    def resolve_files(self, path_list):
        """Generates a single path for the path_list.

        If path_list contains only one path which is a directory or
        multiple paths a .zip is file created else a copy of the file
        is generated.

        Args:
            path_list (list of pathlib.Path)

        Returns:
            str: path to file.
        """
        if len(path_list) == 1 \
        and not path_list[0].is_dir():
            return self.__copy_file(path_list[0])
        else:
            return self._gen_zip(path_list)

    def delete_files(self):
        """Deletes all files copied or created.
        """
        for f in self._deletion_list:
            log.debug(f'delete - {f}.')
            remove(f)
