import requests
import base64

url = "http://127.0.0.1:8000"

# torrentFile string as file contents, post requests

files = {
    'torrentFile': open('data.torrent', 'rb')
}

response = requests.post(url, files=files, verify=False)

print(response.text)
