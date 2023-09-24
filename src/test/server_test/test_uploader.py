import re
import pytest
from server import UploaderFactory
from utils import config, ConfigName


class TestUploader(object):

    @pytest.fixture
    def enable_random_port(self):
        config.set('network', 'RANDOM_PORT', 'True')
        yield
        config.set('network', 'RANDOM_PORT', 'False')

    def test_generated_link_with_settings_defined_port(self, uploader, example_file_path):
        link = uploader.upload_files([example_file_path])
        port = re.match(r'.*:(\d{4})/', link).group(1)
        expected = config.get(ConfigName.NETWORK, ConfigName.PORT)

        assert port == expected

    def test_generated_link_with_random_port_enabled(self, enable_random_port, example_file_path):
        link1 = UploaderFactory.get_uploader().upload_files([example_file_path])
        u = UploaderFactory.get_uploader()
        link2 = u.upload_files([example_file_path])
        u.remove_file_copies()
        port1 = re.match(r'.*:(\d{4})/', link1).group(1)
        port2 = re.match(r'.*:(\d{4})/', link2).group(1)

        assert port1 != port2

    def test_with_one_file_generates_link_to_file(self, uploader, example_file_path, example_file_name):
        link = uploader.upload_files([example_file_path])
        link_last_segment = link.split('/')[-1]

        assert link_last_segment == example_file_name

    def test_with_multiple_files_and_enabled_zip_generates_link_to_zip(self, enable_zip_file, uploader, example_file_paths):
        link = uploader.upload_files(example_file_paths)
        result = re.match(r'.*/download/.*(\.zip)/?$', link)

        assert result != None  # should match FILE.zip

    def test_with_multiple_files_and_disabled_zip_generates_link_to_download_foder(self, disable_zip_file, uploader, example_file_paths):
        link = uploader.upload_files(example_file_paths)
        result = re.match(r'.*/download/?$', link)

        assert result != None  # should match /download/