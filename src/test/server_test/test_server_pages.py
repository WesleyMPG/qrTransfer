from pathlib import Path
from requests import get
from time import sleep
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
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
def multiple_uploaded_file_paths(upload_folder: Path, example_file_names: list[str]):
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


@pytest.fixture
def driver_download_page(selenium: WebDriver, base_url, uploader, example_file_paths: list[Path]):
    uploader.upload_files(example_file_paths)
    selenium.get(f'{base_url}/download/')
    return selenium


def test_upload_page_loading(driver_upload_page: WebDriver):
    assert 'upload' in driver_upload_page.title.lower()


def test_upload_one_file(file_button, upload_button, example_file_path: Path, uploaded_file_path: Path):
    file_button.send_keys(str(example_file_path))
    upload_button.click()

    assert uploaded_file_path.is_file()


def test_upload_multiple_files(file_button, upload_button, example_file_paths: list[Path], multiple_uploaded_file_paths: list[Path]):
    for path in example_file_paths:
        file_button.send_keys(str(path))
    upload_button.click()

    for path in multiple_uploaded_file_paths:
        assert path.is_file()


def test_download_one_file(uploader, base_url: str, example_file_name: str, example_file_path: Path):
    uploader.upload_files([example_file_path])
    response_status_code = get(f'{base_url}/download/{example_file_name}').status_code

    assert response_status_code == 200


def test_download_page_has_only_the_intended_files(driver_download_page: WebDriver, example_file_names):
    items_list = driver_download_page.find_elements(By.CLASS_NAME, 'list-item')
    get_last_segment = lambda l: l.split('/')[-1]
    items_names = [get_last_segment(n.get_attribute('href')) for n in items_list]
    
    for name in items_names:
        assert name in example_file_names


def test_download_multiple_files(driver_download_page: WebDriver, example_file_names: list[str], multiple_uploaded_file_paths):
    btn = driver_download_page.find_element(By.ID, 'download')
    btn.click()
    sleep(time_to_wait_for_files_download(len(example_file_names)))
    for f in multiple_uploaded_file_paths:
        assert f.is_file()


def time_to_wait_for_files_download(n):
    return 5 + n // 3