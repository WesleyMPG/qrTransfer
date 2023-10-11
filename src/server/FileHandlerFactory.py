from .FileHandler import FileHandler
from pathlib import Path
from utils.config import config


class FileHandlerFactory(object):

    @staticmethod
    def get_file_handler():
        static_folder = Path(config.get_static_folder())
        zip_files = config.get_zip_files().as_bool()
        return FileHandler(static_folder, zip_files)