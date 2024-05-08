#!/usr/bin/env python3

from flask import Flask, request
from werkzeug.utils import secure_filename
import subprocess
import os
import uuid

def check_submission(path):
    try:
        if subprocess.call(["./av", path], timeout=3) == 1:
            return "FLAGGED"
    except:
        pass
    return subprocess.check_output([path])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1025 * 1024

@app.route("/")
def index():
    return "POST your binaries for scanning to /scan."

@app.route("/scan", methods=['POST'])
def scan():
    if 'file' not in request.files:
        return 'No files submitted'
    file = request.files['file']
    if not file:
        return "No file?"
    path = os.path.join("uploads", uuid.uuid4().hex)
    try:
        file.save(path)
        os.chmod(path, 0o700)
        return check_submission(path)
    except:
        return "Error"
    finally:
        os.unlink(path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
