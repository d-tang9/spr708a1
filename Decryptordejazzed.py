import os
import glob
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Function to decrypt a .jazz file and restore its original file extension
def decrypt_file(file_path, key):
    try:
        # Check that the file ends with .jazz
        if not file_path.endswith('.jazz'):
            print(f"Skipping {file_path}: not a .jazz file")
            return
        
        # Read the encrypted file
        with open(file_path, 'rb') as file:
            iv = file.read(16)  # Read the initialization vector (first 16 bytes)
            encrypted_data = file.read()  # Read the rest of the encrypted data

        # Create an AES cipher object using the key and the IV
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt and unpad the data
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # Restore the original file path (removing the .jazz extension)
        original_file_path = file_path[:-5]  # Remove the '.jazz' extension

        # Write the decrypted data back to the original file
        with open(original_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        # Remove the .jazz file
        os.remove(file_path)

        print(f"Decrypted {file_path} and restored to {original_file_path}")

    except (PermissionError, FileNotFoundError, IsADirectoryError, ValueError) as e:
        # Handle specific errors and continue to the next file
        print(f"Error decrypting {file_path}: {e}")

# Function to get all .jazz files in a specific directory
def get_jazz_files(directory):
    return glob.glob(os.path.join(directory, '**', '*.jazz'), recursive=True)

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

# Use the same key that was used for encryption
key_hex = 'faa4c5dd46c20d79359f208bbfeb0b3e'  # Replace with the actual key in hex format
key = bytes.fromhex(key_hex)  # Convert hex string to bytes

# Iterate over all possible drives from A:/ to Z:/
for drive_letter in range(ord('A'), ord('Z') + 1):
    drive = chr(drive_letter)
    try:
        if drive_exists(drive):
            print(f"Searching for .jazz files in {drive}")
            jazz_files = get_jazz_files(drive + ":/")
            
            # Decrypt each .jazz file
            for jazz_file in jazz_files:
                decrypt_file(jazz_file, key)
        else:
            print(f"Skipping drive {drive} as it does not exist or is not accessible.")
    except Exception as e:
        print(f"Error while processing drive {drive}: {e}")

# Decryption process is complete
print("Decryption completed.")
