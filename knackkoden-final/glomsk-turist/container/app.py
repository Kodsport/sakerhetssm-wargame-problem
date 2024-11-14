import flask
from flask import request

app = flask.Flask(__name__)

FLAG1 = "SSM{skibidi_viruset_är_ingen_lek}"
FLAG2 = "SSM{sydkorea_fixar_biffen_on_skibidi}"


@app.route("/")
def index():
    return flask.render_template(
        "index.html",
        image_name="challenge1.png",
        guess_url="/guess1",
        next_name="andra utmaningen",
        next_url="/andra",
        desc="Skibidi-viruset har infekterat Svante och du behöver hitta platsen där fotot nedan togs.",
    )


@app.route("/andra")
def andra():
    return flask.render_template(
        "index.html",
        image_name="challenge2.png",
        guess_url="/guess2",
        next_name="första utmaningen",
        next_url="/",
        desc="Svante behöver verkligen botemedlet nu, hjälp honom hitta platsen där fotot nedan togs.",
    )


@app.route("/guess1", methods=["POST"])
def guess1():
    CORRECT_LAT = round(63.3463821, 3)
    CORRECT_LNG = round(13.4601362, 3)

    data = request.get_json()

    lat = round(data["lat"], 3)
    lng = round(data["lng"], 3) % 360

    if lat != CORRECT_LAT or lng != CORRECT_LNG:
        return flask.jsonify({"success": False, "error": "Wrong coordinates!"})

    return flask.jsonify({"success": True, "flag": FLAG1})


@app.route("/guess2", methods=["POST"])
def guess2():

    CORRECT_LAT = round(37.517913, 3)
    CORRECT_LNG = round(127.0965655, 3)

    data = request.get_json()

    lat = round(data["lat"], 3)
    lng = round(data["lng"], 3) % 360

    if lat != CORRECT_LAT or lng != CORRECT_LNG:
        return flask.jsonify({"success": False, "error": "Wrong coordinates!"})

    return flask.jsonify({"success": True, "flag": FLAG2})


@app.route("/static/<path:filename>")
def serve_static(filename):
    return flask.send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
