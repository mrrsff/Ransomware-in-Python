import os
import shutil

from cryptography.fernet import Fernet

os.system('CLS')

if not os.path.exists("Encrypted"):
    print("No encrpted file found. Terminating program.")
    exit()

if not os.path.exists("key.yek"):
    key = input("Please enter the key provided: ")
else:
    with open("key.yek") as thekey:
        lines = thekey.readlines()
        key = lines[0][7:-2]
        id = lines[-1][4:-1]
while 1:
    inId = input("Please enter provided ID: ")
    if inId == id:
        print("ID is true. Proceeding...")
        break
    elif inId == "exit":
        exit()
    else:
        print("Wrong ID. Please enter again or write exit to exit.")

myKey = Fernet(key)

files = []
for file in os.listdir("Encrypted"):
    files.append(file)

if not os.path.exists("Decrypted"):
    os.mkdir("Decrypted")

for i in range(len(files)):
    print(i+1, "of", len(files), "recovered.", end="\r")
    with open("Decrypted\\" + files[i][:-6], "wb") as decrypted:
        with open("Encrypted\\"+files[i]) as locked:
            _data = bytes(locked.read(), "utf-16")
            data = myKey.decrypt(_data)
            decrypted.write(data)

shutil.rmtree("Encrypted")
print("\n")
print("All files decrypted successfully.")