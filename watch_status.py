import os
import socket
import urllib.request, json
from time import sleep
import logging

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

IRCCAT = "localhost:12345"

def get_status():
    with urllib.request.urlopen("https://57north.org.uk/spaceapi") as url:
        data = json.load(url)
        return data["state"]
    
def irc_send(message):
    logger.debug("sending: "+message)
    host, port = IRCCAT.split(":")
    port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        s.sendall(message.encode() + b"\n")
        s.close()
    except socket.timeout:
        logger.info("Timeout connecting to irccat")
    except socket.error as e:
        logger.info("Error sending IRC message (%s): %s", message, e)

try:
    os = get_status()
except:
    os = {"lastchange": 0}

timeout = 10
while True:
    try:
        sleep(timeout)
        s = get_status()
        if not s["lastchange"] == os["lastchange"]:
            os = s
            if s["open"]:
                action = "opened"
            else:
                action = "closed"
            who = s["trigger_person"]
            msg = s["message"]
            irc_send(f"#57N {who} {action} the space: {msg}")
        timeout = 10
    except KeyboardInterrupt:
        exit()
    except Exception as inst:
        logger.exception(inst)
        timeout = min(timeout*2, 600)
        
    
