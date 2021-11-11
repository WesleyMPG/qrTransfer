import sys, re
from os import getenv
from pathlib import Path
from socket import gethostname, gethostbyname

__all__ = ['get_local_network_ip', 'get_program_dir', 'ROOT_DIR']


def get_program_dir():
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


def get_local_network_ip():
    """Returns your computer local ip.

    Returns:
        str
    """
    hostname = gethostname()
    return gethostbyname(hostname)
    

#: Path to src directory
ROOT_DIR : Path = Path(__file__).absolute().parent.parent