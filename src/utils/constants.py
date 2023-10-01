
ZIP_FILE_NAME = 'qrTransfer-files.zip'
CONFIG_FILE_NAME = 'config.ini'


class ConfigName:
    DIRECTORIES = 'directories'
    STATIC_FOLDER = 'STATIC_FOLDER'
    UPLOAD_FOLDER = 'UPLOAD_FOLDER'

    NETWORK = 'network'
    PORT = 'PORT'
    RANDOM_PORT = 'RANDOM_PORT'

    SAVING = 'saving'
    ZIP_FILES = 'ZIP_FILES'

    STRUCTURE = {
        DIRECTORIES: [STATIC_FOLDER, UPLOAD_FOLDER],
        NETWORK: [PORT, RANDOM_PORT],
        SAVING: [ZIP_FILES],
    }