import sys, re
from pathlib import Path
from socket import gethostname, gethostbyname

__all__ = ['get_local_network_ip', 'get_program_dir', 'ROOT_DIR']


def get_program_dir():
    """Get program dir path.

    Detects if what is running is the executable or not and return
    it's real path.

    Returns:
        str: dir path.
    """
    if getattr(sys, 'frozen', False):
        folder = Path(sys.executable).parent
        return folder.absolute().resolve()
    else:
        folder = Path(__file__).absolute()
        folder = folder.joinpath('..').resolve()
        return folder.parent


def resource_path(relative):  #TODO: remove
    try:
        base = sys._MEIPASS
    except (IsADirectoryError, AttributeError):
        base = Path('..').resolve().absolute()
    return base.joinpath(relative)


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
    

#: Path to src directory
ROOT_DIR : Path = Path(__file__).absolute().parent.parent