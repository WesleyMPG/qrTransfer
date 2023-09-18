from .FileHandler import FileHandler
from pathlib import Path
from utils import config


class FileHandlerFactory(object):

    @staticmethod
    def get_file_handler():
        static_folder = Path(config['directories']['STATIC_FOLDER'])
        zip_files = config.getboolean('saving', 'ZIP_FILES')
        return FileHandler(static_folder, zip_files)