import requests
import websocket

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

class WebServer:
    def __init__(self, uri, csrf_token, sessionid) -> None:
        self.connection = websocket.WebSocket()
        cookie = f"csrftoken={csrf_token}; sessionid={sessionid}"
        self.connection.connect(f"ws://{HOST}/ws/{uri}",cookie=cookie)
        
