from threading import Thread
import requests as req
from flask import Flask, request, send_file, redirect, flash, render_template
from werkzeug.utils import secure_filename
import os

__all__ = ['Server']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/wesley/Downloads/'
app.secret_key = os.urandom(16).hex()

@app.route('/status-check/')
def hello_world():
    return 'working'


@app.route('/download/<path:path>')
def download(path):
    return send_file(f'static/{path}')


@app.route('/sdwn/')
def shutdown():
    shut = request.environ.get("werkzeug.server.shutdown")

    if shut is None:
        raise RuntimeError("Not running the development server.")

    shut()
    return 'Done'



class Server(object):
    @staticmethod
    def run():
        """Creates the server thread
        """
        server = Thread(
            target=lambda:app.run(debug=False,
                                  use_reloader=False,
                                  host='0.0.0.0'),
            daemon=True
        )
        server.start()

    @staticmethod
    def is_up():
        try:
            r = req.get('http://localhost:5000/status-check/')
            return True
        except req.exceptions.ConnectionError:
            return False


if __name__ == "__main__":
    app.run(debug=False,
            use_reloader=True,
            host='0.0.0.0')

