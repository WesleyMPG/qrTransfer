import sys, os, signal
from pathlib import Path
import pytest

src = Path(__file__).parent.parent
sys.path.append(str(src))

from server import Server
from utils import config


PORT = config.get('network', 'PORT')
BASE_URL = f'http://localhost:{PORT}'


@pytest.fixture
def firefox_options(firefox_options):
    # firefox_options.add_argument('-headless')
    return firefox_options


@pytest.fixture(scope='session')
def base_url():
    return BASE_URL


@pytest.fixture(scope='session', autouse=True)
def server():
    pid = Server.run()
    yield
    Server.stop()


@pytest.fixture
def example_file_names():
    return ['simple_file.txt', 'simple_file2.txt', 'simple_file3.txt',]


@pytest.fixture
def empty_folder_name():
    return 'empty_folder'


@pytest.fixture
def create_empty_folder(tmp_path, empty_folder_name):
    ed = tmp_path / empty_folder_name
    ed.mkdir()


@pytest.fixture
def one_file_path(shared_datadir, example_file_names):
    return shared_datadir / example_file_names[0]


@pytest.fixture
def multiple_file_paths(shared_datadir, example_file_names):
    paths = map(lambda p: shared_datadir / p, example_file_names)
    return list(paths)


@pytest.fixture
def one_file_name(example_file_names):
    return example_file_names[0]


@pytest.fixture
def example_file(one_file_path):
    with open(str(one_file_path)) as file:
        yield file


@pytest.fixture
def disable_zip_file():
    config.set('saving', 'ZIP_FILES', 'False')


@pytest.fixture
def enable_zip_file():
    config.set('saving', 'ZIP_FILES', 'True')


