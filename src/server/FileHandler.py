import os.path as osp, logging
from os import walk as os_walk, remove
from pathlib import Path
from zipfile import ZipFile
from shutil import copy2
from werkzeug.utils import secure_filename
from utils.constants import ZIP_FILE_NAME


log = logging.getLogger(f'Main.{__name__}')


class FileHandler(object):

    def __init__(self, static_folder : Path, zip_files=True):
        self._out_dir = static_folder
        self._zip_out = static_folder.joinpath(ZIP_FILE_NAME)
        self._zip_files = zip_files
        self._deletion_list = []
    
    def resolve_files(self, path_list : [Path]):
        """Generates the path or path list for the copied files.

        If path_list contains only one path which is a directory or
        multiple paths and ZIP_FILES is true, a .zip is file created, 
        else a copy of the file(s) is generated.

        Args:
            path_list (:obj:`list` of :obj:`pathlib.Path`)

        Returns:
            [str]: paths to files.
        """
        if len(path_list) == 0: return [self._out_dir]
        if len(path_list) == 1 and not path_list[0].is_dir():
            return [self.__copy_file(path_list[0])]
        elif not self._zip_files:
            return self.__copy_all_files(path_list)
        else:
            return [self._gen_zip(path_list)]
        
    def __copy_file(self, path : Path) -> Path:
        """Makes a copy to static_folder.

        It copies the file and adds its path to _deletion_list
        
        Args:
            path (pathlib.Path)
        """
        file_name = secure_filename(path.name)
        file_path = self._out_dir / file_name
        copy2(path, file_path)
        log.debug(f'copy - {path} copied to {file_path}.')
        self._deletion_list.append(file_path)
        return file_path
        
    def __copy_all_files(self, path_list: [Path]) -> list[Path]:
        tmp = []
        for path in path_list:
            t = self.__copy_file(path)
            tmp.append(t)
        return tmp

    def _gen_zip(self, path_list) -> Path:
        """Generates a zip file.

        returns:
            The path to the zip file.
        """
        with ZipFile(self._zip_out, 'w') as z:
            for path in path_list:
                log.debug(f'zip - {path}.')
                if path.is_dir():
                    self.__zip_a_dir(str(path), z)
                else:
                    z.write(path, path.name)
        self._deletion_list.append(self._zip_out)
        return self._zip_out
    
    def __zip_a_dir(self, path, zip_file):
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

    def delete_files(self):
        """Deletes all files copied or created.
        """
        for f in self._deletion_list:
            log.debug(f'delete - {f}.')
            remove(f)
