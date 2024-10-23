import json
import os
from flask import Flask, render_template, jsonify, request, make_response
from bot import playwright_bot

app = Flask(__name__)

admin_secret = os.urandom(32).hex()

css_templates = [
    """#container {font-family: "Arial", "sans-serif";color: greenyellow;}""",
    """#container {font-family: "BlackOpsOne", "sans-serif";background-image: url(static/backgrounds/camo.jpg);color: white;}""",
    """#container {font-family: "GreatVibes", "sans-serif";background-image: url(static/backgrounds/old.jpg);color: black;}""",
    """#container {font-family: "IndieFlower", "sans-serif";background-image: url(static/backgrounds/flower.jpg);color: blue;}""",
    """#container {font-family: "LibreBarcode39", "sans-serif";background-image: url(static/backgrounds/alien.jpg);background-size: contain;color: red; }""",
    """#container {font-family: "SortsMillGoudy", "sans-serif";background-image: url(static/backgrounds/blueberry.jpg);background-size: contain;color: tomato;}""",
    """#container {font-family: "PressStart2P", "sans-serif";background-image: url(static/backgrounds/game.jpg);background-size: contain;color: black; }""",
]

default_theme = {"css": css_templates[0]}


def validate_css(css):
    if css.count("{") == 1 and css.count("}") == 1:
        return True
    return False


@app.route("/")
def index_route():
    return render_template("index.html")


@app.route("/create")
def create_route():
    return render_template("create.html")


@app.route("/view")
def view_route():
    theme = request.cookies.get("theme")
    resp = make_response(render_template("view.html"))

    if not theme:
        resp.set_cookie("theme", json.dumps(default_theme), httponly=True)
        return resp

    if not validate_css(json.loads(theme)["css"]):
        return jsonify({"msg": "Nej"})

    return resp


@app.route("/theme")
def theme_route():
    return render_template("theme.html")


@app.route("/api/theme")
def get_theme():
    theme = request.cookies.get("theme")
    return jsonify(json.loads(theme)) if theme else jsonify(default_theme)


@app.route("/api/theme", methods=["POST"])
def post_theme():
    json_data = request.get_json()
    theme = json.loads(request.cookies.get("theme", "{}"))

    secret = json_data.get("secret", "")
    if secret and secret == admin_secret:
        theme["css"] = "#container {" + json_data.get("css") + "}"
    elif secret:
        return jsonify({"msg": "Felaktig nyckel!"})
    else:
        theme["css"] = css_templates[int(json_data.get("css", "0"))]

    resp = jsonify({"msg": "Temat uppdaterades framgångsrikt!"})
    resp.set_cookie("theme", json.dumps(theme), httponly=True, **request.args)

    return resp


@app.route("/api/bot")
def bot():
    kebab = request.args.get("kebab")
    if not kebab:
        return jsonify({"msg": "Du skickade ingen kebab!"})
    if len(kebab) > 400:
        return jsonify({"msg": "Kebaben är för lång!"})
    res = playwright_bot("http://127.0.0.1:5000/view?" + kebab, admin_secret)
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
