import sys
from os import getenv, name as os_name
from pathlib import Path
from socket import gethostname, gethostbyname


def get_program_dir() -> Path:
    """Get program dir path.

    Detects if what is running is the executable or not and return
    it's real path.

    Returns:
        pathlib.Path: dir path.
    """
    if getattr(sys, 'frozen', False):
        folder = Path(sys.executable).parent
        return folder.absolute().resolve()
    else:
        folder = Path(__file__).absolute()
        folder = folder.joinpath('..').resolve()
        return folder.parent


def get_logs_dir():
    """Returns logs dir path.

    Returns:
        pathlib.Path
    """
    return get_local_dir().joinpath('logs')


def get_local_dir():
    if os_name == 'nt':
        f = Path(getenv('LOCALAPPDATA')).joinpath('qrTransfer')
    else:
        f = get_program_dir()
    if not f.exists(): f.mkdir(parents=True)
    return f


def get_local_network_ip():
    """Returns your computer local ip.

    Returns:
        str
    """
    hostname = gethostname()
    return gethostbyname(hostname)
    

#: Path to src directory
ROOT_DIR : Path = Path(__file__).absolute().parent.parent
