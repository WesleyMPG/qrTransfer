import os
import requests as req
from threading import Thread
from werkzeug.utils import secure_filename
from flask import Flask, request, send_file, redirect, flash, render_template
from utils import config


__all__ = ['Server']


STATIC_FOLDER = config['directories']['STATIC_FOLDER']
UPLOAD_FOLDER = config['directories']['UPLOAD_FOLDER']
PORT = config['network']['PORT']

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.secret_key = os.urandom(16).hex()


@app.route('/status-check/')
def hello_world():
    return 'working'


@app.route('/download/<path:path>')
def download(path):
    return send_file(f'{STATIC_FOLDER}/{path}')


@app.route('/sdwn/')
def shutdown():
    shut = request.environ.get("werkzeug.server.shutdown")

    if shut is None:
        raise RuntimeError("Not running the development server.")

    shut()
    return 'Done'


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            folder = UPLOAD_FOLDER
            save_path = os.path.join(folder, filename)
            file.save(save_path)
            return render_template('upload.html', mode='done')
    return render_template('upload.html', mode='pick')


class Server(object):
    @staticmethod
    def run():
        """Creates the server thread
        """
        server = Thread(
            target=lambda:app.run(debug=False,
                                  use_reloader=False,
                                  host='0.0.0.0',
                                  port=int(PORT)),
            daemon=True
        )
        server.start()

    @staticmethod
    def is_up():
        try:
            r = req.get(f'http://localhost:{PORT}/status-check/')
            return True
        except req.exceptions.ConnectionError:
            return False


if __name__ == "__main__":
    app.run(debug=False,
            use_reloader=True,
            host='0.0.0.0')

