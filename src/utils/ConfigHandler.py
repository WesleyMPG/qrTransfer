import logging, configparser, sys
from pathlib import Path
from .constants import ConfigName
from utils import get_program_dir

__all__ = ['config']

log = logging.getLogger(f'Main.{__name__}')


class ConfigHandler(object):
    def __init__(self, file_path):
        """This class is responsable for load the config file and
        validate its content.

        Args:
            file_path (pathlib.Path)
        """
        self._config = None
        self._file_path = Path(file_path)
        self._load_file()
    
    @property
    def config(self):
        """A dict containing all settings.

        Returns:
            dict of {str: dict of {str: any}}: all settings.
        """
        return self._config
    
    def __assert_config(self):
        self.__assert_structure()
        self.__assert_folders()
        self.__assert_network()

    def __assert_structure(self):
        for s in ConfigName.STRUCTURE.keys():
            if s not in self._config.sections():
                log.error(f'"{s}" section missing at config file.')
                sys.exit(1)
            for i in ConfigName.STRUCTURE[s]:
                if i not in self._config[s]:
                    log.error(f'"{i}" missing at "{s}" config.')
                    sys.exit(1)

    def __assert_folders(self): 
        dirs = self._config[ConfigName.DIRECTORIES]
        for k in dirs.keys():
            dirs[k] = str(Path(dirs[k]).absolute())

        static = Path(dirs[ConfigName.STATIC_FOLDER])
        log.debug(f'folders - Static folder: {static}.')
        if not static.is_dir(): 
            log.warning(f"Static folder doesn't exists. Creating it...")
            static.mkdir()

        upload = Path(dirs[ConfigName.UPLOAD_FOLDER])
        log.debug(f'folders - Upload folder: {upload}.')
        if not upload.is_dir():
            upload.mkdir(parents=True)
            log.info(f'Upload folder created at {upload}')

    def __assert_network(self):
        ntw = self._config[ConfigName.NETWORK]

        log.debug(f'network - Port: {ntw["PORT"]}')
        if not ntw[ConfigName.PORT].isdecimal():
            log.warning('Invalid port value. Setting default...')
            ntw[ConfigName.PORT] = '5000'
        if not ntw[ConfigName.RANDOM_PORT] in ['True', 'False']:
            log.warning('Invalid value for for RANDOM_PORT config.')
            ntw[ConfigName.RANDOM_PORT] = 'False'
        
    def _load_file(self):
        log.info("Loading config file.")
        self._config = configparser.ConfigParser()
        self._config.read(self._file_path)
        self.__assert_config()
        
    def save_config(self):
        log.info("Saving config file.")
        with open(self._file_path, 'w') as f:
            self._config.write(f)


config_handler = ConfigHandler(get_program_dir().joinpath('config.ini'))
config = config_handler.config