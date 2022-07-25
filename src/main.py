import qrcode as qr
from time import sleep
from server import Server, UploaderFactory
from utils import get_local_network_ip, config, args, logger
from PIL import Image as PIL_Image


class QrTransfer(object):
    PORT = config['network']['PORT']

    def __init__(self):
        self.__qrCode_params = {
            'box_size': 10,
            'border': 2,
        }
    
    def run(self):
        self.__start_server()
        self.__start_transfer_mode()

    def __start_server(self):
        """Start and wait for server to be up."""
        Server.run()
        while not Server.is_up():
            sleep(1)        

    def __start_transfer_mode(self):
        if args.pc_to_mobile:
            self.__start_pc_to_mobile_mode()
        else:
            self.__start_mobile_to_pc_mode()

    def __start_pc_to_mobile_mode(self):
        from display import qr_window
        u = UploaderFactory.getUploader(args.shall_remote_upload)
        link = u.upload(args.path_list)
        code = self.__generate_qrCode(link)
        qr_window(code, at_close=u.remove_file_copies)

    def __start_mobile_to_pc_mode(self):
        from display import qr_window
        code = self.__generate_mobile_to_pc_code()
        qr_window(code)

    def __generate_mobile_to_pc_code(self):
        ip = get_local_network_ip()
        link = f'http://{ip}:{QrTransfer.PORT}/upload/'
        return self.__generate_qrCode(link)

    def __generate_qrCode(self, text) -> PIL_Image:
        code = qr.QRCode(**self.__qrCode_params)
        code.add_data(text)
        code.make(fit=True)
        return code.make_image()


if __name__ == "__main__":
    try:
        QrTransfer().run()
    except Exception as e:
        logger.exception('An unexpected behavior ocurred.')

