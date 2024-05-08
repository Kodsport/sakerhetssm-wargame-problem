import os
import yaml
from pathlib import Path

html = Path("index.html").read_bytes()
yamimgs = [
    Path("yam1.jpg").read_bytes(),
    Path("yam2.jpg").read_bytes(),
    Path("yam3.jpg").read_bytes(),
]
prices = [5, 25, 50]


# this is a raw WSGI app
def app(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]
    cookies = {
        cookie.split("=")[0].strip(): cookie.split("=")[1].strip()
        for cookie in environ.get("HTTP_COOKIE", "").split(";")
        if cookie != ""
    }
    money = int(cookies.get("money", 100))
    inventory = [int(i) for i in cookies.get("inventory", "").split(":") if i != ""]

    if path == "/" and method == "GET":
        response_body = html.replace(
            b"$$INVENTORY$$",
            "".join(
                [
                    f"""<img src="yam{i}.jpg" class="card-img-top" style="max-width: 15rem">"""
                    for i in inventory
                ]
            ).encode(),
        ).replace(b"$$MONEY$$", str(money).encode())

        start_response(
            "200 OK",
            [
                ("Content-Type", "text/html"),
                ("Content-Length", str(len(response_body))),
                ("Set-Cookie", f"money={money}"),
                (
                    "Set-Cookie",
                    f'inventory={":".join([str(i) for i in inventory])}',
                ),
            ],
        )
        return [response_body]

    if (
        path.startswith("/yam")
        and path.endswith(".jpg")
        and len(path) == 9
        and method == "GET"
    ):
        if "HTTP_IF_NONE_MATCH" in environ:
            start_response(
                "304 Not Modified",
                [],
            )
            return []

        response_body = yamimgs[int(path[4]) - 1]

        start_response(
            "200 OK",
            [
                ("Content-Type", "text/html"),
                ("Content-Length", str(len(response_body))),
                ("Etag", str(int(path[4]) - 1)),
            ],
        )
        return [response_body]

    if path == "/buy" and method == "POST":
        form = environ["wsgi.input"].read().decode()
        parsed_form = yaml.load(form.replace("&", "\n").replace("=", ": "), yaml.Loader)

        price = prices[parsed_form.get("yam", 0)]

        if money - price < 0:
            start_response(
                "402 Payment Required",
                [
                    ("Content-Type", "text/plain"),
                    ("Content-Length", str(len(b"Not enough money!"))),
                ],
            )
            return [b"Not enough money!"]

        money -= price
        inventory.append(parsed_form.get("yam", 0) + 1)

        start_response(
            "302 Found",
            [
                ("Set-Cookie", f"money={money}"),
                (
                    "Set-Cookie",
                    f'inventory={":".join([str(i) for i in inventory])}',
                ),
                ("Location", "/"),
                ("Content-Type", "text/plain"),
                ("Content-Length", str(len(str(parsed_form).encode()))),
            ],
        )
        return [str(parsed_form).encode()]  # for debug

    start_response(
        "404 Not Found",
        [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(b"Not found"))),
        ],
    )
    return [b"Not found"]
