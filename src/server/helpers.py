import os
from pathlib import Path
import logging
from werkzeug.utils import secure_filename
from flask import flash
from utils import config

STATIC_FOLDER = config.get('directories', 'STATIC_FOLDER')
UPLOAD_FOLDER = Path(config.get('directories', 'UPLOAD_FOLDER'))
server_log = logging.getLogger('Main.server.py')


def list_files_to_download():
    files = []
    for path in os.scandir(STATIC_FOLDER):
        if path.is_file():
            files.append(path.name)
    return files


def were_files_selected(files):
    if files[0].filename != '': return True
    flash('No file selected.')
    server_log.info('upload - No file selected.')
    return False

def save_files(files):
    for file in files:
        filename = secure_filename(file.filename)
        save_path = UPLOAD_FOLDER / filename
        save_file(file, save_path)
        

def save_file(file, path):
    file.save(path)
    server_log.info(f'upload - saved at {path}.')