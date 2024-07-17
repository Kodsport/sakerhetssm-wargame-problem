import json
import pymongo
from flask import Flask, render_template, request, abort

client = pymongo.MongoClient()

with open(__file__) as f:
    source = f.read()

db = client["ss"]
collection = db["books"]

application = Flask(__name__)


@application.route("/", methods=["GET"])
def home():
    return render_template("home.html", books=collection.find({"borrowed": False}))


@application.route("/book", methods=["GET"])
def book():
    try:
        return render_template(
            "book.html",
            book=collection.find_one({"id": json.loads(request.args.get("id"))}),
        )
    except:
        return abort(400)


@application.route("/source", methods=["GET"])
def source_view():
    return source


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000, threaded=False)
