import requests
import websocket
import threading
import json

HOST = "http://127.0.0.1:8000"

# sync con

#gets
def get_api(url_ending, params):
    res = requests.get(HOST+url_ending, params)
    if res.ok:
        return res.json()

def get_roles():
    res = get_api("/roles", {})
    return res


#posts
class Client:
    def __init__(self) -> None:
        self.client = requests.Session()
    
    def post_auth(self, username):
        content = {"username" : username}
        res = self.client.post(HOST + "/auth", content)
        if res.ok:
            self.csrf = res.cookies["csrftoken"]
            print(res.cookies)
            self.session = res.cookies["sessionid"]

            return res.json()
    
    def post_role_id(self, id):
        URL = HOST + "/role_submission"
        content = {"id" : id, "csrfmiddlewaretoken" : self.csrf}
        res = self.client.post(URL, content)
        if res.ok :
            return res.json()
        return False

    def get_game(self):
        url = HOST + "/get_game"
        res = self.client.get(url)
        if res.ok:
            return res.json()
        return False
    
    def get_game_info(self):
        url = HOST + "/get_game_info"
        res = self.client.get(url)
        if res.ok:
            return res.json()

class WebServer:
    def __init__(self, uri, screen) -> None:
        self.screen = screen
        self.client = screen.client
        self.submited   = False
        self.connection = websocket.WebSocket()
        cookie = f"csrftoken={self.client.csrf}; sessionid={self.client.session}"
        self.connection.connect(f"ws://127.0.0.1:8000/ws/{uri}",cookie=cookie)
        threading.Thread(target=self.ws_listening).start()

    def submit_action(self, btn_data):
        if not self.submited:
            data = json.dumps({
                "type" : "submit",
                "action": btn_data
            })
            self.connection.send(data)
            self.submited = True

    def ws_listening(self):
        while self.connection:
            recv = self.connection.recv()
            recv = json.loads(recv)
            if recv["type"] == "status":
                if recv["status"] == "started":
                    self.screen.game_info["status"] = "started"
                    self.screen.game_info = self.client.get_game_info()

                if recv["status"] == "new":
                    self.submited = False 
                    self.screen.game_info = self.client.get_game_info()                    
                    print("SSSSSSSSSSSS")

            else:
                print(recv)