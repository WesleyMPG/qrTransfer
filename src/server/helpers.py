import os
from utils import config

STATIC_FOLDER = config['directories']['STATIC_FOLDER']


def list_files_to_download():
    files = []
    for path in os.scandir(STATIC_FOLDER):
        if path.is_file():
            files.append(path.name)
    return files