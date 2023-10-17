"""
Nabil Abdel-Rahman's Flask API.
"""

import os
from flask import Flask, abort, send_from_directory, render_template
import configparser

def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
DEBUG = config["SERVER"]["DEBUG"]
PORT = config["SERVER"]["PORT"]

app = Flask(__name__)

@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

@app.route("/<string:filepath>")
def index(filepath):
    path = 'pages/' + filepath
    if '..' in filepath or '~' in filepath:
        abort(403)
    elif not os.path.exists(path):
        abort(404)
    else:
        return send_from_directory('pages/', filepath), 200

@app.errorhandler(403)
def error_403(e):
    return send_from_directory('pages/', '403.html'), 403

@app.errorhandler(404)
def error_404(e):
    return send_from_directory('pages/', '404.html'), 404

if __name__ == "__main__":
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)