import pytest
from os import listdir as os_listdir
from server.FileHandler import FileHandler
from utils.constants import ZIP_FILE_NAME


class TestFileHandler(object):


    @pytest.fixture
    def file_handler_with_resolved_files(self, tmp_path, multiple_file_paths):
        file_handler = FileHandler(tmp_path, zip_files=False)
        file_handler.resolve_files(multiple_file_paths)
        return file_handler

    def test_resolve_files_with_no_files(self, tmp_path):
        file_handler = FileHandler(tmp_path)
        result = file_handler.resolve_files([])
        assert result == [tmp_path]

    def test_resolve_files_with_one_file(self, tmp_path, example_file, example_file_path, example_file_names):
        file_handler = FileHandler(tmp_path)
        result = file_handler.resolve_files([example_file_path])

        assert len(result) == 1
        assert result == [tmp_path / example_file_names[0]]
        with open(result[0]) as result_file:
            assert result_file.readlines() == example_file.readlines()
    
    def test_resolve_files_with_one_file_and_no_zip_files(self, tmp_path, example_file_path, example_file_names):
        file_handler = FileHandler(tmp_path, zip_files=False)
        result = file_handler.resolve_files([example_file_path])

        expected_file_path = [tmp_path / example_file_names[0]]
        assert result == expected_file_path

    def test_resolve_files_with_multiple_files_and_zip_files(self, tmp_path, multiple_file_paths):
        file_handler = FileHandler(tmp_path, zip_files=True)
        result = file_handler.resolve_files(multiple_file_paths)

        expected_zipped_file_path = [tmp_path / ZIP_FILE_NAME]
        assert result == expected_zipped_file_path

    def test_resolve_files_with_multiple_files_and_no_zip_files(self, tmp_path, multiple_file_paths, example_file_names):
        file_handler = FileHandler(tmp_path, zip_files=False)
        result = file_handler.resolve_files(multiple_file_paths)

        expected_list_of_file_paths = list(map(lambda p: tmp_path / p, example_file_names))
        assert result == expected_list_of_file_paths

    def test_resolve_files_with_empty_folder_and_zip_files(self, tmp_path, create_empty_folder, empty_folder_name):
        file_handler = FileHandler(tmp_path)
        result = file_handler.resolve_files([tmp_path / empty_folder_name])

        expected_zipped_file_path = [tmp_path / ZIP_FILE_NAME]
        assert result == expected_zipped_file_path

    def test_delete_files_after_resolved_files(self, tmp_path, file_handler_with_resolved_files, example_file_names):
        count_before_delete = len(os_listdir(tmp_path))
        file_handler_with_resolved_files.delete_files()
        count_after_delete = len(os_listdir(tmp_path))

        assert count_before_delete == len(example_file_names) + 1
        assert count_after_delete == 1