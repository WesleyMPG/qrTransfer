from configparser import ConfigParser


class ConfigWrapper(object):
    pass

class WrapperValue(str):
    def as_bool(self):
        if self == 'True':
            return True
        elif self == 'False':
            return False
        raise ValueError(f'Not a boolean: {self}')
    
    def as_int(self):
        if self.isdecimal():
            return int(self)
        raise ValueError(f'Not an integer: {self}')
    
    def as_float(self):
        try:
            return float(self)
        except ValueError:
            raise ValueError(f'Not a float: {self}')


class ConfigWrapperGenerator(object):
    UPPER_CASE_INDICATOR = '^'
    def __init__(self, config_dict : dict | ConfigParser):
        self._config = config_dict
        self._wrapper = ConfigWrapper()
        self._field_and_section = self._invert_section_and_field_relation()

    def _invert_section_and_field_relation(self):
        field_and_section = {}
        for section in self._config.keys():
            for field_name in self._config[section].keys():
                self.__add_section_to_fields_list_of_sections(field_and_section, field_name, section)
        return field_and_section

    @staticmethod
    def __add_section_to_fields_list_of_sections(field_and_section : dict, field : str, section : str):
        field, section = ConfigWrapperGenerator.__mark_section_if_field_is_upper_case(field, section)
        if field_and_section.get(field) is None:
            field_and_section[field] = []
        field_and_section[field].append(section)

    @staticmethod
    def __mark_section_if_field_is_upper_case(field: str, section: str) -> tuple[str]:
        if field.isupper():
            field = field.lower()
            section += ConfigWrapperGenerator.UPPER_CASE_INDICATOR
        return field, section

    def gen(self) -> ConfigWrapper:
        for field in self._field_and_section.keys():
            self._create_methods_for_all_occurrences_of_this_field(field, self._field_and_section[field])
        return self._wrapper
    
    def _create_methods_for_all_occurrences_of_this_field(self, field : str, sections_that_has_this_field : list[str]):
        is_field_name_duplicated = len(sections_that_has_this_field) > 1
        for section in sections_that_has_this_field:
            core_name = self.__get_core_name(section, field, is_field_name_duplicated)
            self._create_wrapper_methods(section, field, core_name)

    @staticmethod
    def __get_core_name(section, field, is_field_name_duplicated):
        if section[-1] == ConfigWrapperGenerator.UPPER_CASE_INDICATOR:
            section = section[:-1]
        core_name = f'{section}_{field}' if is_field_name_duplicated else f'{field}'
        return core_name.lower().replace('-', '_')

    def _create_wrapper_methods(self, section : str, field_name : str, core_name : str):
        g_and_s = self._gen_getter_and_setter(section, field_name)
        setattr(self._wrapper, f'get_{core_name}', g_and_s[0])
        setattr(self._wrapper, f'set_{core_name}', g_and_s[1])

    def _gen_getter_and_setter(self, section : str, field_name : str):
        section, field_name = self.__check_for_upper_case_field(section, field_name)
        def getter() -> WrapperValue:
            return WrapperValue(self._config[section][field_name])
        def setter(v):
            self._config[section][field_name] = v
        return (getter, setter)
    
    @staticmethod
    def __check_for_upper_case_field(section: str, field: str) -> tuple[str]:
        if section[-1] == ConfigWrapperGenerator.UPPER_CASE_INDICATOR:
            section = section[:-1]
            field = field.upper()
        return section, field
