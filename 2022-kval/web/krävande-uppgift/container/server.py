from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "/KDgW{bFIu^Fh[zSn*(4hLOA5QGMmcRV~6IM5csE"

usernames_and_passwords = {"admin": "AB12Q46WWlol811"}

secret_flag = "SSM{myck37_und3rl164_kr4v}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        login_message = "Grattis, du lyckades logga in! "
        if username == "admin":
            login_message += "Här har du en flagga: " + secret_flag
        else:
            login_message += "Tyvärr har jag inte någon flagga åt dig, eftersom att du inte loggade in med \"admin\" som användarnamn..."

        if username in usernames_and_passwords:
            if usernames_and_passwords[username] == password:
                return render_template("success.html", message=login_message)
            else:
                flash("Ogiltigt lösenord!")
        else:
            flash("Ogiltig användare!")

    return render_template("login.html")


@app.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username in usernames_and_passwords:
            flash("Den användaren finns redan registrerad!")

        else:
            error_message = check_password_requirements(password)
            if error_message:
                flash(error_message)
            else:
                usernames_and_passwords[username] = password
                return redirect(url_for("index"))

    return render_template("register.html")


def check_password_requirements(password):
    if len(password) < 15:
        return "Lösenordet måste vara minst 15 tecken långt"
    if len(password) > 15:
        return "Lösenordet får inte vara mer än 15 tecken långt"

    allowed_chars = "ABCDEFGHJLMOPQRSUVWXZabcdeghijklmnorsuvwyz1245689"
    for char in password:
        if char not in allowed_chars:
            return f"Endast följande tecknen är tillåtna i lösenordet: {allowed_chars}"

    if not any(c in password[-3:] for c in "0123456789"):
        return "De sista tre tecknen i lösenordet måste vara siffror"

    if not password[0:2].isupper():
        return "Det första och andra tecknet i lösenordet måste vara versaler"

    if not password[4] == "Q":
        return "Det femte tecknet i lösenordet måste vara ett Q"

    if "lol" not in password:
        return "Ordet \"lol\" måste finnas med i lösenordet"

    if ord(password[0]) + ord(password[1]) + ord(password[2]) != 180:
        return "Summan av ascii-värdena på de första tre tecknen måste vara 180"

    if password[7] != password[8]:
        return "Det åttonde och nionde tecknet i lösenordet måste vara samma"

    chars = [x for x in password[0:8]]
    if len(set(chars)) != len(chars):
        return "De första åtta tecknen i lösenordet får inte vara sammma"

    if sum(ord(password[i]) for i in range(5,9)) != 280:
        return "Summan av ascii-värdena på tecken nummer 6, 7, 8 och 9 måste vara 280"

    if int(password[-3:]) < 800:
        return "Lösenordet måste sluta på ett tresiffrigt tal som är större än 800"

    if sum(ord(c) for c in password) != 1072:
        return "Summan av ascii-värdena på alla tecken i lösenordet måste vara 1072"

    return ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

