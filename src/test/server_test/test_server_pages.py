from time import sleep
from pathlib import Path
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


@pytest.fixture
def driver_upload_page(selenium: WebDriver, base_url: str) -> WebDriver:
    selenium.get(f'{base_url}/upload')
    return selenium


@pytest.fixture
def uploaded_file_path(upload_folder: Path, example_file_name) -> Path:
    file: Path = upload_folder / example_file_name
    yield file
    if file.is_file(): file.unlink()


@pytest.fixture
def multiple_uploaded_files_path(upload_folder: Path, example_file_names: list[str]):
    files = list(map(lambda name: upload_folder / name, example_file_names))
    yield files
    for f in files:
        if f.is_file(): f.unlink()


@pytest.fixture
def file_button(driver_upload_page: WebDriver):
    return driver_upload_page.find_element(By.ID, 'file')


@pytest.fixture
def upload_button(driver_upload_page: WebDriver):
    return driver_upload_page.find_element(By.ID, 'submit')


def test_upload_page_loading(driver_upload_page: WebDriver):
    assert 'upload' in driver_upload_page.title.lower()


def test_upload_one_file(file_button, upload_button, example_file_path: Path, uploaded_file_path: Path):
    file_button.send_keys(str(example_file_path))
    upload_button.click()

    assert uploaded_file_path.is_file()


def test_upload_multiple_files(file_button, upload_button, multiple_file_paths: list[Path], multiple_uploaded_files_path: list[Path]):
    for path in multiple_file_paths:
        file_button.send_keys(str(path))
    upload_button.click()

    for path in multiple_uploaded_files_path:
        assert path.is_file()