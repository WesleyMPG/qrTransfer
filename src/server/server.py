import os, logging, signal
from time import sleep
from pathlib import Path
import requests as req
from threading import Thread
from flask import Flask, request, send_file, redirect, render_template
from utils import config, ConfigName
from .helpers import list_files_to_download, were_files_selected, save_files


__all__ = ['Server']

log = logging.getLogger(f'Main.{__name__}')

STATIC_FOLDER = config.get(ConfigName.DIRECTORIES, ConfigName.STATIC_FOLDER)
PORT = config.get(ConfigName.NETWORK, ConfigName.PORT)
SHUTDOWN_WAIT_TIME = 2

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.secret_key = os.urandom(16).hex()


@app.route('/status-check/')
def hello_world():
    return 'working'


@app.route('/test_shutdown/')
def trigger_sutdown():
    st = Thread(target=shutdown, args=[os.getpid()], daemon=True)
    st.start()
    return f"<h1>This route is meant for testing purposes. Shutting down in {SHUTDOWN_WAIT_TIME} seconds</h1>"
    

def shutdown(pid):
    sleep(SHUTDOWN_WAIT_TIME)
    os.kill(pid, signal.SIGSTOP)


@app.get('/download/')
def multidownload():
    """File download function

    Args:
        paths (list): List of paths to the files. Usually just their names. 

    Returns:
        The files.
    """
    files = list_files_to_download()
    log.debug(f'multidownload - Files: {files}.')
    return render_template('download.html', files=files)


@app.route('/download/<path:path>')
def download(path):
    """File download function

    Args:
        path (str): Path to the file. Usually just its name. 

    Returns:
        The file.
    """
    log.debug(f'download - File: {path}.')
    return send_file(f'{Path(STATIC_FOLDER).joinpath(path)}',
                     download_name=f'{path}',
                     as_attachment=True,
    )
    

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    """Upload function

    Returns:
        Upload page.
    """
    if request.method == 'GET':
        return render_template('upload.html', mode='pick')

    if 'file' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('file')
    if not were_files_selected(files):
        return
    save_files(files)
    return render_template('upload.html', mode='done')


class Server(object):
    @staticmethod
    def run():
        """Creates the server thread
        """
        log.info('Stating server...')
        server = Thread(
            target=lambda:app.run(debug=True,
                                  use_reloader=False,
                                  host='0.0.0.0',
                                  port=int(PORT)),
            daemon=True
        )
        server.start()

    @staticmethod
    def is_up():
        """It's a way to check if server is up

        Returns:
            bool: True if working.
        """
        try:
            r = req.get(f'http://localhost:{PORT}/status-check/')
            return True
        except req.exceptions.ConnectionError:
            return False

    @staticmethod
    def stop():
        try:
            req.get(f'http://localhost:{PORT}/test_shutdown/')
        except req.exceptions.ConnectionError:
            pass


if __name__ == "__main__":
    app.run(debug=True,
            use_reloader=True,
            host='0.0.0.0')

