import re
import pytest
from server import UploaderFactory


class TestUploader(object):


    def test_with_one_file_generates_link_to_file(self, example_file_path, example_file_name):
        uploader = UploaderFactory.get_uploader()
        link = uploader.upload_files([example_file_path])
        link_last_segment = link.split('/')[-1]

        assert link_last_segment == example_file_name

    def test_with_multiple_files_and_enabled_zip_generates_link_to_zip(self, example_file_paths, enable_zip_file):
        uploader = UploaderFactory.get_uploader()
        link = uploader.upload_files(example_file_paths)
        result = re.match(r'.*/download/.*(\.zip)/?$', link)

        assert result != None  # should match FILE.zip

    def test_with_multiple_files_and_disabled_zip_generates_link_to_download_foder(self, example_file_paths, disable_zip_file):
        uploader = UploaderFactory.get_uploader()
        link = uploader.upload_files(example_file_paths)
        result = re.match(r'.*/download/?$', link)

        assert result != None  # should match /download/