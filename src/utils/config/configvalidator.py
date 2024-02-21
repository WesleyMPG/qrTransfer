import logging
from configparser import ConfigParser, NoSectionError, NoOptionError
from .constants import STRUCTURE
from .config_generator import get_default_config


class ConfigValidator(object):
    def __init__(self, structure: dict, default_config: ConfigParser):
        self._log = logging.getLogger(f'Main.{__name__}')
        self._structure = structure
        self._default_config = default_config
        self._validate_default_config()
        self._invalid_fields: list[tuple[str]] = None

    def _validate_default_config(self):
        if not self.is_structure_valid(self._default_config):
            raise InvalidDefaultConfigError(self._invalid_fields[0])

    def validate_config(self, config):
        if self.is_structure_valid(config): return
        self._set_default_on_invalid_values()

    def is_structure_valid(self, config: ConfigParser) -> bool:
        self._config = config
        self._invalid_fields = []
        self.__walk_on_structure()
        return (len(self._invalid_fields) == 0)

    def __walk_on_structure(self):
        for section in self._structure.keys():
            self.__walk_on_section_fields(section)

    def __walk_on_section_fields(self, section: str):
        for field, _type in self._structure[section]:
            self.__validate_value(section, field, _type)

    def __validate_value(self, section, field, _type):
        if self.__is_value_present(section, field):
            value = self._config.get(section, field)
            if self._is_value_valid(value, _type): return
        self._mark_invalid_field(section, field)

    def __is_value_present(self, section, field):
        try:
            self._config.get(section, field)
            return True
        except (NoOptionError, NoSectionError):
            return False

    @staticmethod
    def _is_value_valid(value: str, _type):
        if _type == int:
            return value.isdecimal()
        elif _type == bool:
            return (value == 'True' or value == 'False')
        elif _type == float:
            return ConfigValidator.__is_float(value)
        elif _type == str:
            return True
        else:
            raise BadTypeError(_type)

    @staticmethod
    def __is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def _mark_invalid_field(self, section: str, field: str):
        self._invalid_fields.append((section, field))

    def _set_default_on_invalid_values(self):
        for section, field in self._invalid_fields:
            self._set_default(section, field)
            self._log.warning(f'The value in [{section.upper()}] {field.upper()} is invalid. The default value will be used.')

    def _set_default(self, section, field):
        try:
            self._config[section][field] = self._default_config[section][field]
        except KeyError:
            self._config[section] = {field: self._default_config[section][field]}


class BadTypeError(Exception):
     def __init__(self, _type, *args, **kwargs):
        message = f'Bad type: {_type} is not a valid type for a config structure.'
        super().__init__(message, *args, **kwargs)


class InvalidDefaultConfigError(Exception):
    def __init__(self, invalid, *args, **kwargs):
        message = f'The provided default config doesn\'t follow the provided structure: {invalid}'
        super().__init__(message, *args, **kwargs)


class ConfigValidatorFactory:
    @staticmethod
    def get_config_validator():
        return ConfigValidator(STRUCTURE, get_default_config())