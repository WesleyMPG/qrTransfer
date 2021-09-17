import qrcode as qr
from time import sleep
from cli import file_path
from server import Server, Uploader
from display import window


def qr_gen(text):
    """Creates the qrcode image
    """
    return qr.make(text).convert('RGB')


def main():
    print('Uploading file...')
    u = Uploader(mode=Uploader.LOCAL_MODE)
    link = u.upload(file_path)

    code = qr_gen(link)

    Server.run()
    while not Server.is_up():
        sleep(1)
    window(code, at_close=u.done)


if __name__ == "__main__":
    main()

