import os
import socket
import urllib.request, json
from time import sleep

IRCCAT = "localhost:12345"

def get_status():
    with urllib.request.urlopen("https://57north.org.uk/spaceapi") as url:
        data = json.load(url)
        return data["state"]
    
def irc_send(message):
    host, port = IRCCAT.split(":")
    port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        s.sendall(message.encode() + b"\n")
        s.close()
    except socket.timeout:
        print("Timeout connecting to irccat")
    except socket.error as e:
        print("Error sending IRC message (%s): %s", message, e)

os = get_status()
        
while True:
    sleep(10)
    s = get_status()
    if not s["lastchange"] == os["lastchange"]:
        os = s
        if s["open"]:
            action = "openeed"
        else:
            action = "closed"
        who = s["trigger_person"]
        msg = s["message"]
        irc_send(f"#57N {who} {action} the space: {msg}")
    
