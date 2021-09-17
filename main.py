import qrcode as qr
from time import sleep
from cli import args
from server import Server, Uploader
from display import window
from utils import get_local_network_ip


def qr_gen(text):
    """Creates the qrcode image
    """
    return qr.make(text).convert('RGB')


def start_server():
    Server.run()
    while not Server.is_up():
        sleep(1)


def upload_mode():
    """Make a file available to be downloaded
    """
    print('Uploading file...')
    u = Uploader(mode=Uploader.LOCAL_MODE)
    link = u.upload(args.path)
    code = qr_gen(link)
    window(code, at_close=u.done)


def download_mode():
    ip = get_local_network_ip()
    return f'http://{ip}:5000/upload/'


def main():
    start_server()

    if args.pc_to_mobile:
        upload_mode()
    else:
        link = download_mode()
        code = qr_gen(link)
        window(code)


if __name__ == "__main__":
    main()

