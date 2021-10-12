from socket import gethostname, gethostbyname
import configparser, logging
import os, sys, re

__all__ = ['get_local_network_ip', 'resource_path', 'config',
            'ROOT_DIR']

log = logging.getLogger(__name__)


def get_program_dir():
    """Get program dir path.

    Detects if what is running is the executable or not and return
    it's real path.

    Returns:
        str: dir path.
    """
    if getattr(sys, 'frozen', False):
        folder = os.path.dirname(sys.executable)
        return os.path.abspath(folder)
    else:
        folder = os.path.abspath(__file__)
        return os.path.dirname(folder)


def resource_path(relative):
    try:
        base = sys._MEIPASS
    except (IsADirectoryError, AttributeError):
        base = os.path.abspath('.')
    return os.path.join(base, relative)


def __get_ip_on_windows():  #TODO: remove
    sub = subprocess.run(
        ['cmd.exe', '/c', 'ipconfig | findstr IPv4'],
        stdout=subprocess.PIPE)
    ip = sub.stdout.decode('latin1')
    ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
    return ip


def __get_ip_on_unix():  #TODO: remove
    sub = subprocess.Popen(
        "hostname -I | awk '{print $1}'",
        shell=True, stdout=subprocess.PIPE)
    ip = sub.stdout.read()[:-1].decode()
    return ip


def get_local_network_ip():
    """Returns your computer local ip.

    Returns:
        str
    """
    hostname = gethostname()
    return gethostbyname(hostname)
    

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

        log.debug(f'ConfigHandler - folders - Static folder: {dirs["STATIC_FOLDER"]}.')
        if not os.path.isdir(dirs['STATIC_FOLDER']): 
            log.warning(f"Static folder doesn't exists. Creating it...")
            static = dirs['STATIC_FOLDER']
            os.mkdir(static)

        log.debug(f'ConfigHandler - folders - Upload folder: {dirs["UPLOAD_FOLDER"]}.')
        if not os.path.isdir(dirs['UPLOAD_FOLDER']):
            log.error(f'Upload folder doesn\'t exists.')
            sys.exit(1)

    def __assert_network(self):
        ntw = self._config['network']
        log.debug(f'ConfigHandler - network - Port: {ntw["PORT"]}')
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
        log.info("ConfigHandler - Loading config file.")
        config = configparser.ConfigParser()
        config.read(file_path)
        self._config = config
        self.__assert_config()

            
config = ConfigHandler(
    os.path.join(get_program_dir(), 'config.ini'))

#: Path to src directory
ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__))