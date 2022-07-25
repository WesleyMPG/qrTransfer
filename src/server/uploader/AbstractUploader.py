from server import FileHandler


class AbstractUploader(object):

    def __init__(self, log):
        self.__log = log
        self.__fhandler = FileHandler()
        
    def upload_files(self, path_list):
        self.__log.debug(f'upload - type: {type(self)}.')
        link = self.__get_link(path_list) 
        self.__log.debug(f'upload - Link: {link}.')
        return link

    def remove_file_copies(self):
        self.__fhandler.delete_files()
    
    def _get_link(self, path_list):
        pass
