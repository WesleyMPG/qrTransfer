from .FileHandler import FileHandler
from pathlib import Path
from utils import config_obj, ConfigName


class FileHandlerFactory(object):

    @staticmethod
    def get_file_handler():
        static_folder = Path(config_obj.get(ConfigName.DIRECTORIES, ConfigName.STATIC_FOLDER))
        zip_files = config_obj.getboolean(ConfigName.SAVING, ConfigName.ZIP_FILES)
        return FileHandler(static_folder, zip_files)