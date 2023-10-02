from configparser import ConfigParser
import pytest
from utils.config.configwrapper import ConfigWrapperGenerator, ConfigWrapper


@pytest.fixture
def config_dict() -> dict:
    cp = ConfigParser()
    cp['section1'] = {
            'stt1': '1',
            'stt2': 'False',
        }
    return cp


@pytest.fixture
def config_dict_with_duplicate() -> dict:
    return {
        'section1': {
            'stt1': '1',
            'stt2': '2',
        },
        'section2': {
            'stt1': '4',
            'stt3': '3',
        },
    }


@pytest.fixture
def config_dict_with_special_cases() -> dict:
    return {
        'SECTION1': {
            'STT1': '1',
            'stt-2': '2',
        },
    }


@pytest.fixture
def config_dict_with_duplicate_and_uppder_case() -> dict:
    return {
        'section1': {
            'stt1': '1',
        },
        'section2': {
            'STT1': '4',
        },
    }

@pytest.fixture
def config_wrapper(config_dict):
    return ConfigWrapperGenerator(config_dict).gen()


def test_gen_config_wrapper_instance(config_dict):
    config_wrapper = ConfigWrapperGenerator(config_dict).gen()
    assert isinstance(config_wrapper, ConfigWrapper)


def test_config_wrapper_contains_config_values_acessors(config_wrapper, config_dict):
    assert config_wrapper.get_stt1() == config_dict['section1']['stt1']
    config_wrapper.set_stt1('11')
    assert config_wrapper.get_stt1() == '11'


def test_special_config_names(config_dict_with_special_cases):
    config_wrapper = ConfigWrapperGenerator(config_dict_with_special_cases).gen()
    assert config_wrapper.get_stt1() == config_dict_with_special_cases['SECTION1']['STT1']
    assert config_wrapper.get_stt_2() == config_dict_with_special_cases['SECTION1']['stt-2']


def test_duplicated_config_names_are_merged_with_section_name(config_dict_with_duplicate):
    config_wrapper = ConfigWrapperGenerator(config_dict_with_duplicate).gen()
    assert config_wrapper.get_section1_stt1() == config_dict_with_duplicate['section1']['stt1']
    assert config_wrapper.get_section2_stt1() == config_dict_with_duplicate['section2']['stt1']
    config_wrapper.set_section1_stt1('11')
    config_wrapper.set_section2_stt1('44')


def test_duplicated_config_and_uppder_case_name(config_dict_with_duplicate_and_uppder_case):
    config_wrapper = ConfigWrapperGenerator(config_dict_with_duplicate_and_uppder_case).gen()
    assert config_wrapper.get_section1_stt1() == config_dict_with_duplicate_and_uppder_case['section1']['stt1']
    assert config_wrapper.get_section2_stt1() == config_dict_with_duplicate_and_uppder_case['section2']['STT1']


def test_config_as_boolean(config_wrapper):
    assert config_wrapper.get_stt2().as_bool() == False
    with pytest.raises(ValueError):
        config_wrapper.get_stt1().as_bool()


def test_config_as_int(config_wrapper, config_dict):
    assert config_wrapper.get_stt1().as_int() == int(config_dict['section1']['stt1'])
    with pytest.raises(ValueError):
        config_wrapper.get_stt2().as_int()


def test_config_as_float(config_wrapper, config_dict):
    assert config_wrapper.get_stt1().as_float() == float(config_dict['section1']['stt1'])
    with pytest.raises(ValueError):
        config_wrapper.get_stt2().as_float()