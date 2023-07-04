
from . import views
import threading

websocket_pattern = {
    "command" : "function",
    "foo"     : views.foo,
    "join"    : views.join,
    "ask_info": views.get_info,
    "submit_role"   : views.submit_role,
    "post_action"   : views.action,
}


def manage_connection(client, addr):

    while True:
        command = client.recv_command()
        if command:
            function = websocket_pattern[command["command"]]
            command["args"]["socket"] = client
            threading.Thread(target=function, args=(command["args"],)).start()
            
        else: 
            print(f"[DETACHED]: connection lost with {addr}")
            client.close()
            break
            




#{"command" : "command_name",
# "args": {
#       arg1:foo,
#       arg2:bar,
# }}


#{"command": "join",
#args : {"socket" : client}
#}