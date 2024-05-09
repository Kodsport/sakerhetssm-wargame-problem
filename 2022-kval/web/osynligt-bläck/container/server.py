from flask import *

app = Flask(__name__)

flag = "SSM{nja_kanske_inte_helt_osynlig}"

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

