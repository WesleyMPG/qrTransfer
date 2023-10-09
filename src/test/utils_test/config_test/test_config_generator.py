import pytest
from utils.config.config_generator import write_config_file, get_upload_folder, get_static_folder


@pytest.fixture
def config_file_path(tmp_path):
    file_path = tmp_path / 'test_config.ini'
    yield file_path
    if file_path.exists():
        file_path.unlink()


def test_create_file(config_file_path):
    if config_file_path.exists(): config_file_path.unlink()
    write_config_file(config_file_path)
    assert config_file_path.exists()


def test_get_upload_folder_path_on_unix(mocker):
    mocker.patch('utils.config.config_generator.os_name', return_value='posix')
    path = get_upload_folder()
    assert path.find('/') != -1


def test_get_upload_folder_path_on_windows(mocker):
    mocker.patch('utils.config.config_generator.os_name', return_value='nt')
    path = get_upload_folder()
    assert path.find('\\') != -1


def test_get_static_folder_path_on_unix(mocker):
    mocker.patch('utils.config.config_generator.os_name', return_value='posix')
    path = get_static_folder()
    assert path.find('/') != -1


def test_get_static_folder_path_on_windows(mocker):
    mocker.patch('utils.config.config_generator.os_name', return_value='nt')
    path = get_static_folder()
    assert path.find('\\') != -1