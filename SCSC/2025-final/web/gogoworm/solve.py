import requests


host = 'http://localhost:8080'
s = requests.session()

resp = s.post(host+'/register', data='{"Name":"okokokok", "Password": "okokokok"}')
print("register", resp.status_code, resp.text)


resp = s.post(host+'/login', data='{"Name":"okokokok", "Password": "okokokok"}', allow_redirects=False)
print("login", resp.status_code, resp.text)
print("cookies", resp.cookies)

resp = s.post(host+'/buy', data='{"ProductID": 1, "User": { "Name":"xyz", "Password": "xyz", "Money": 126, "SessionID": "hej"} }')
print("buy", resp.status_code, resp.text)



resp = requests.post(host+'/buy', data='{"ProductID": 3 }', cookies={"gogoworm": "hej"})
print("buy", resp.status_code, resp.text)
