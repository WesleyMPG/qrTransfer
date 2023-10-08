from configparser import ConfigParser
import pytest
from utils.config.configvalidator import ConfigValidator, BadTypeError


@pytest.fixture(scope='module')
def config():
    config = ConfigParser()
    config['section1'] = {
        'stt1': '1',
        'stt2': '2.3',
    }
    config['section2'] = {
        'stt3': 'True'
    }
    return config


@pytest.fixture(scope='module')
def default_config():
    return {
        'section1': { 'stt1': '5','stt2': '3', 'stt3': 'True' },
        'section3': { 'stt6': 'True' },
        'section4': { 'stt7': '3.2' }
    }


@pytest.fixture(scope='module')
def structure():
    return {
        'section1': [('stt1', int), ('stt2', float)],
        'section2': [('stt3', bool)],
    }


@pytest.fixture(scope='module')
def config_validator(structure):
    return ConfigValidator(structure)


@pytest.fixture(scope='module')
def structure2():
    return {
        'section1': [('stt1', int), ('stt4', str)],
        'section2': [('stt2', float), ('stt3', bool)]
    }


@pytest.fixture(scope='module')
def structure3():
    return {
        'section1': [('stt1', int), ('stt2', int), ('stt3', bool)],
        'section3': [('stt6', bool)],
        'section4': [('stt7', float)],
    }


@pytest.fixture(scope='module')
def structure4():
    return {
        'section1': [('stt1', int), ('stt2', int)],
        'section2': [('stt3', bool)],
    }


def test_validate_config_structure(config, structure, default_config):
    cv = ConfigValidator(structure, default_config)
    assert cv.is_structure_valid(config)
    

def test_invalid_structure_different_fields(config, structure2, default_config):
    cv = ConfigValidator(structure2, default_config)
    assert cv.is_structure_valid(config) == False


def test_invalid_structure_different_sections(config, structure3, default_config):
    cv = ConfigValidator(structure3, default_config)
    assert cv.is_structure_valid(config) == False


def test_invalid_structure_wrong_types(config, structure4, default_config):
    cv = ConfigValidator(structure4, default_config)
    assert cv.is_structure_valid(config) == False


def test_value_and_type_assertion():
    assert ConfigValidator._is_value_valid('True', bool)
    assert ConfigValidator._is_value_valid('1.1', float)
    assert ConfigValidator._is_value_valid('12', int)


def test_value_and_type_assertion_wrong_types():
    assert ConfigValidator._is_value_valid('True', int) == False
    assert ConfigValidator._is_value_valid('False', float) == False
    assert ConfigValidator._is_value_valid('1.1', int) == False
    assert ConfigValidator._is_value_valid('1.1', bool) == False
    assert ConfigValidator._is_value_valid('123', bool) == False


def test_value_and_type_assertion_bad_type():
    with pytest.raises(BadTypeError):
        ConfigValidator._is_value_valid('12', object)


def test_validate_config(config, structure3, default_config):
    cv = ConfigValidator(structure3, default_config)
    cv.validate_config(config)
    assert config['section1']['stt1'] == '1'  # valid value
    assert config['section1']['stt2'] == default_config['section1']['stt2']  # invalid type
    assert config['section1']['stt3'] == default_config['section1']['stt3']  # missing only one value
    assert config['section3']['stt6'] == default_config['section3']['stt6']  # missing section and value