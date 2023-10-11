import logging, configparser
from pathlib import Path
from ..constants import CONFIG_FILE_NAME
from .config_generator import write_config_file
from .configvalidator import ConfigValidator, ConfigValidatorFactory
from .configwrapper import ConfigWrapperGenerator, ConfigWrapper
from utils import get_program_dir


__all__ = ['config_handler', 'config']

log = logging.getLogger(f'Main.{__name__}')


class ConfigHandler(object):
    def __init__(self, config_file_path: Path, config_parser: configparser.ConfigParser, config_validator: ConfigValidator):
        self._file_path = config_file_path
        self._config = config_parser
        self._validator = config_validator
        self._wrapper = None

    def get_config(self) -> ConfigWrapper:
        if self._wrapper is None:
            self._load_config()
        return self._wrapper

    def _load_config(self):
        self._create_file_if_not_exist()
        self._config.read(self._file_path)
        self._validator.validate_config(self._config)
        self._wrapper = ConfigWrapperGenerator(self._config).gen()

    def save_config(self):
        log.info("Saving config file.")
        with open(self._file_path, 'w') as f:
            self._config.write(f)

    def _create_file_if_not_exist(self):
        if self._file_path.exists(): return True 
        write_config_file(self._file_path)
        return False


class ConfigHandlerFactory:

    @staticmethod
    def get_config_handler():
        file_path = get_program_dir() / CONFIG_FILE_NAME
        config_parser = configparser.ConfigParser()
        config_validator = ConfigValidatorFactory.get_config_validator()
        return ConfigHandler(file_path, config_parser, config_validator)
    

config_handler = ConfigHandlerFactory.get_config_handler()
config = config_handler.get_config()