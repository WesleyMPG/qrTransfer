import sys
from pathlib import Path
import pytest

src = Path(__file__).parent.parent
sys.path.append(str(src))

from server import Server, UploaderFactory
from utils import config


PORT = config.get('network', 'PORT')
BASE_URL = f'http://localhost:{PORT}'
UPLOAD_FOLDER = Path(config.get('directories', 'UPLOAD_FOLDER'))


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument('-headless')
    firefox_options.set_preference("browser.download.dir", str(UPLOAD_FOLDER))
    return firefox_options


@pytest.fixture(scope='session')
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope='session', autouse=True)
def server():
    Server.run()
    yield
    Server.stop()


@pytest.fixture
def upload_folder() -> Path:
    return UPLOAD_FOLDER


@pytest.fixture
def uploader():
    u = UploaderFactory.get_uploader()
    yield u
    u.remove_file_copies()


@pytest.fixture
def empty_folder_name() -> str:
    return 'empty_folder'


@pytest.fixture
def empty_folder_path(tmp_path: Path, empty_folder_name) -> Path:
    ed: Path = tmp_path / empty_folder_name
    ed.mkdir()
    yield ed
    ed.rmdir()


@pytest.fixture
def example_file_names() -> list[str]:
    return ['simple_file.txt', 'simple_file2.txt', 'simple_file3.txt',]


@pytest.fixture
def example_file_name(example_file_names):
    return example_file_names[0]


@pytest.fixture
def example_file_path(shared_datadir, example_file_names) -> Path:
    return shared_datadir / example_file_names[0]


@pytest.fixture
def example_file_paths(shared_datadir, example_file_names) -> list[Path]:
    paths = map(lambda p: shared_datadir / p, example_file_names)
    return list(paths)


@pytest.fixture
def example_file(example_file_path):
    with open(str(example_file_path)) as file:
        yield file


@pytest.fixture
def disable_zip_file():
    config.set('saving', 'ZIP_FILES', 'False')


@pytest.fixture
def enable_zip_file():
    config.set('saving', 'ZIP_FILES', 'True')


