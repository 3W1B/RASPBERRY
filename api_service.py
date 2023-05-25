import http.client
import json


class ApiService:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def post(self, body):
        conn = http.client.HTTPConnection(self.host, self.port)
        payload = json.dumps(body)
        headers = {
            'Content-Type': "application/json",
        }
        conn.request("POST", "/log/create", payload, headers)
        response = conn.getresponse()
        data = response.read()
        return data.decode("utf-8")