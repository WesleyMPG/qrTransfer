

class AbstractUploader(object):

    def __init__(self, file_handler, log):
        self._log = log
        self._fhandler = file_handler
        self._uploaded_files = []

        
    def upload_files(self, path_list):
        self._log.debug(f'upload - type: {type(self)}.')
        link = self._get_link(path_list) 
        self._log.debug(f'upload - Link: {link}.')
        return link

    def remove_file_copies(self):
        self._uploaded_files = []
        self._fhandler.delete_files()
    
    def _get_link(self, path_list):
        pass
