from socket import gethostname, gethostbyname
import configparser
import os, sys, re

__all__ = ['get_local_network_ip', 'resource_path', 'config',
            'ROOT_DIR']


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


def config_setup():
    """Read settings in config.ini.

    Returns:
        dict of {str: dict of {str: str}}: all settings.
    """
    config = configparser.ConfigParser()
    this_dir = get_program_dir()
    config.read(os.path.join(this_dir, 'config.ini'))
    return config

config = config_setup()


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
    


def assert_folders():  #TODO: create a exception here
    dirs = config['directories']
    for k in dirs.keys():
        dirs[k] = os.path.abspath(dirs[k])
    if not os.path.isdir(dirs['STATIC_FOLDER']):
        os.mkdir(dirs['STATIC_FOLDER'])
    if not os.path.isdir(dirs['UPLOAD_FOLDER']):
        print(f'{dirs["UPLOAD_FOLDER"]} is not a directorie.')
        sys.exit(1)


assert_folders()

#: Path to src directory
ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__))