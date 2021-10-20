import logging, configparser, sys, os
from utils import get_program_dir

__all__ = ['config']

log = logging.getLogger(f'Main.{__name__}')


class ConfigHandler(object):
    def __init__(self, file_path):
        self._config = None
        self._load_file(file_path)
    
    @property
    def config(self):
        """A dict containing all settings.

        Returns:
            dict of {str: dict of {str: str}}: all settings.
        """
        return self._config

    def __assert_structure(self):
        structure = {
            'directories': ['STATIC_FOLDER', 'UPLOAD_FOLDER'],
            'network': ['PORT'],
        }
        for s in structure.keys():
            if s not in self._config.sections():
                log.error(f'"{s}" section missing at config file.')
                sys.exit(1)
            for i in structure[s]:
                if i not in self._config[s]:
                    log.error(f'"{i}" missing at "{s}" config.')
                    sys.exit(1)

    def __assert_folders(self): 
        dirs = self._config['directories']
        for k in dirs.keys():
            dirs[k] = os.path.abspath(dirs[k])

        static = dirs["STATIC_FOLDER"]
        log.debug(f'folders - Static folder: {static}.')
        if not os.path.isdir(static): 
            log.warning(f"Static folder doesn't exists. Creating it...")
            os.mkdir(static)

        upload = dirs["UPLOAD_FOLDER"]
        log.debug(f'folders - Upload folder: {upload}.')
        if not os.path.isdir(upload):
            log.error(f'Upload folder doesn\'t exists.')
            sys.exit(1)

    def __assert_network(self):
        ntw = self._config['network']

        log.debug(f'network - Port: {ntw["PORT"]}')
        if not ntw['PORT'].isdecimal():
            log.warning('Invalid port value. Setting default...')
            ntw['PORT'] = '5000'

    def __assert_config(self):
        self.__assert_structure()
        self.__assert_folders()
        self.__assert_network()
        
    def _load_file(self, file_path):
        """Read settings in file_path
        """
        log.info("Loading config file.")
        config = configparser.ConfigParser()
        config.read(file_path)
        self._config = config
        self.__assert_config()


config = ConfigHandler(
    os.path.join(get_program_dir(), 'config.ini')).config