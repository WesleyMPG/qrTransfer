import pytest
from os import listdir as os_listdir
from server.FileHandler import FileHandler
from utils.constants import ZIP_FILE_NAME

class TestFileHandler(object):

    example_file_names = ['simple_file.txt',
                        'simple_file2.txt',
                        'simple_file3.txt',]
    empty_folder_name = 'emtpy_folder'

    @pytest.fixture
    def create_empty_folder(self, tmp_path):
        ed = tmp_path / self.empty_folder_name
        ed.mkdir()

    @pytest.fixture
    def one_file_path(self, shared_datadir):
        return shared_datadir / self.example_file_names[0]
    
    @pytest.fixture
    def multiple_file_paths(self, shared_datadir):
        paths = map(lambda p: shared_datadir / p, self.example_file_names)
        return list(paths)

    @pytest.fixture
    def example_file(self, one_file_path):
        with open(str(one_file_path)) as file:
            yield file

    @pytest.fixture
    def file_handler_with_resolved_files(self, tmp_path, multiple_file_paths):
        file_handler = FileHandler(tmp_path, zip_files=False)
        file_handler.resolve_files(multiple_file_paths)
        return file_handler

    def test_resolve_files_with_no_files(self, tmp_path):
        file_handler = FileHandler(tmp_path)
        result = file_handler.resolve_files([])
        assert result == [tmp_path]

    def test_resolve_files_with_one_file(self, tmp_path, example_file, one_file_path):
        file_handler = FileHandler(tmp_path)
        result = file_handler.resolve_files([one_file_path])

        assert result == tmp_path / self.example_file_names[0]
        with open(result) as result_file:
            assert result_file.readlines() == example_file.readlines()
    
    def test_resolve_files_with_one_file_and_no_zip_files(self, tmp_path, one_file_path):
        file_handler = FileHandler(tmp_path, zip_files=False)
        result = file_handler.resolve_files([one_file_path])

        expected_file_path = tmp_path / self.example_file_names[0]
        assert result == expected_file_path

    def test_resolve_files_with_multiple_files_and_zip_files(self, tmp_path, multiple_file_paths):
        file_handler = FileHandler(tmp_path, zip_files=True)
        result = file_handler.resolve_files(multiple_file_paths)

        expected_zipped_file_path = tmp_path / ZIP_FILE_NAME
        assert result == expected_zipped_file_path

    def test_resolve_files_with_multiple_files_and_no_zip_files(self, tmp_path, multiple_file_paths):
        file_handler = FileHandler(tmp_path, zip_files=False)
        result = file_handler.resolve_files(multiple_file_paths)

        expected_list_of_file_paths = list(map(lambda p: tmp_path / p, self.example_file_names))
        assert result == expected_list_of_file_paths

    def test_resolve_files_with_empty_folder_and_zip_files(self, tmp_path, create_empty_folder):
        file_handler = FileHandler(tmp_path)
        result = file_handler.resolve_files([tmp_path / self.empty_folder_name])

        expected_zipped_file_path = tmp_path / ZIP_FILE_NAME
        assert result == expected_zipped_file_path

    def test_delete_files_after_resolved_files(self, tmp_path, file_handler_with_resolved_files):
        count_before_delete = len(os_listdir(tmp_path))
        file_handler_with_resolved_files.delete_files()
        count_after_delete = len(os_listdir(tmp_path))

        assert count_before_delete == len(self.example_file_names) + 1
        assert count_after_delete == 1