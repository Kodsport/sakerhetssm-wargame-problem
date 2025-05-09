from flask import Flask, Response, request
import hashlib

app = Flask(__name__)

def do_sha256(data):
    hasher = hashlib.sha256()
    hasher.update(data)
    return int.from_bytes(hasher.digest(), byteorder="little")

def hash_login(username, password):
    return (do_sha256(username) * 0x123321 + do_sha256(password) * 0x321123) & 0xffff_ffff_ffff

ADMIN_HASH = 0xf61ea4e5c9c2

@app.route("/login")
def login():
    username = request.args.get("username")
    if username is None:
        return Response("parameter username required!!!!", mimetype="text/plain", status=400)

    password = request.args.get("password")
    if password is None:
        return Response("parameter password required!!!!", mimetype="text/plain", status=400)

    hashed = hash_login(username.encode(), password.encode())

    with open("logged_in.html", "r") as f:
        content = f.read()
        content = content.replace("{username}", f"{username}")
        content = content.replace("{hash}", f"{hex(hashed)}")
        if hashed == ADMIN_HASH:
            with open("secrets.txt", "r") as secrets:
                content = content.replace("{secrets}", secrets.read())
        else:
            content = content.replace("{secrets}", "no secrets for you")

    return Response(content, mimetype="text/html")

@app.route("/")
def index():
    with open("index.html", "r") as f:
        content = f.read()
    return Response(content, mimetype="text/html")

@app.route("/source")
def source():
    with open("server.py", "r") as f:
        content = f.read()
    return Response(content, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
