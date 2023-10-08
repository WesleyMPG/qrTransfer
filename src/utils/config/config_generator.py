import os
from configparser import ConfigParser
from .constants import *


def os_name(): # this way it's possible to mock the OS
    return os.name


def gen_config_file(file_path):
    config_parser = ConfigParser()
    config_parser[DIRECTORIES] = {
        STATIC_FOLDER: get_static_folder(),
        UPLOAD_FOLDER: get_upload_folder(),
    }
    config_parser[NETWORK] = {
        PORT: '5000',
        RANDOM_PORT: 'False',
    }
    with open(file_path, 'w') as config_file:
        config_parser.write(config_file)


def get_static_folder():
    if os_name() == 'nt': 
        return 'C:\\Windows\\temp\\qrTransfer'
    return '/tmp/qrTransfer'


def get_upload_folder():
    if os_name() == 'nt':
        user_name = os.getenv('USERNAME')
        return f'C:\\Users\\{user_name}\\Downloads'
    else:
        home = os.getenv('HOME')
        return f'{home}/Downloads'
    
