import qrcode as qr
from time import sleep
from cli import args
from server import Server, Uploader
from display import qr_window
from utils import get_local_network_ip, config


PORT = config['network']['PORT']


def qr_gen(text):
    """Creates the qrcode image
    """
    code = qr.QRCode(
        box_size=10,
        border=2
    )
    code.add_data(text)
    code.make(fit=True)
    return code.make_image()


def start_server():
    Server.run()
    while not Server.is_up():
        sleep(1)


def upload_mode():
    """Make a file available to be downloaded
    """
    from display import qr_window
    print('Uploading file...')
    if args.remote:
        u = Uploader(mode=Uploader.REMOTE_MODE)
    else:
        u = Uploader(mode=Uploader.LOCAL_MODE)
    link = u.upload(args.path)
    code = qr_gen(link)
    qr_window(code, at_close=u.done)


def download_mode():
    from display import qr_window
    ip = get_local_network_ip()
    link = f'http://{ip}:{PORT}/upload/'
    code = qr_gen(link)
    qr_window(code)


def main():
    start_server()
    if args.pc_to_mobile:
        upload_mode()
    else:
        download_mode()


if __name__ == "__main__":
    main()

