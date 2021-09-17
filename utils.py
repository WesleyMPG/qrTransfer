import subprocess
import configparser
import os

__all__ = ['get_local_network_ip', 'config']


def config_setup():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config['DEFAULT']

config = config_setup()


def get_local_network_ip():
    sub = subprocess.Popen(
        "hostname -I | awk '{print $1}'",
        shell=True, stdout=subprocess.PIPE)
    ip = sub.stdout.read()[:-1].decode()
    return ip


def assert_folders():
    if not os.path.isdir(config['STATIC_FOLDER']):
        os.mkdir(config['STATIC_FOLDER'])



assert_folders()
