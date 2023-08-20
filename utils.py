import os
import platform
import keyboard
import time

# Load namelist
def loadNameList(filepath,encoding="utf-8") -> list:
    if os.path.exists(filepath):
        content = open(filepath,'r',encoding=encoding).read()
        content = content.strip("\n")
        content = content.strip()
        nameList = content.split(",")
        return nameList
    else:
        raise Exception(f"Namelist-file: {filepath} not found and won't be loaded!")

# Keyboard reader functions
def waitKey(keyname):
    keyname = str(keyname)
    while True:
        if keyboard.is_pressed(keyname):
            keyboard.release(keyname)
            time.sleep(0.1)
            return True
def waitchoice(key1,key2):
    key1 = str(key1)
    key2 = str(key2)
    while True:
        if keyboard.is_pressed(key1):
            keyboard.release(key1)
            time.sleep(0.1)
            return key1
        if keyboard.is_pressed(key2):
            keyboard.release(key2)
            time.sleep(0.1)
            return key2
def waitchoice3(key1,key2,key3):
    key1 = str(key1)
    key2 = str(key2)
    key3 = str(key3)
    while True:
        if keyboard.is_pressed(key1):
            keyboard.release(key1)
            time.sleep(0.1)
            return key1
        if keyboard.is_pressed(key2):
            keyboard.release(key2)
            time.sleep(0.1)
            return key2
        if keyboard.is_pressed(key3):
            keyboard.release(key3)
            time.sleep(0.1)
            return key3
def waitchoice4(key1,key2,key3,key4):
    key1 = str(key1)
    key2 = str(key2)
    key3 = str(key3)
    key4 = str(key4)
    while True:
        if keyboard.is_pressed(key1):
            keyboard.release(key1)
            time.sleep(0.1)
            return key1
        if keyboard.is_pressed(key2):
            keyboard.release(key2)
            time.sleep(0.1)
            return key2
        if keyboard.is_pressed(key3):
            keyboard.release(key3)
            time.sleep(0.1)
            return key3
        if keyboard.is_pressed(key4):
            keyboard.release(key4)
            time.sleep(0.1)
            return key4

# Debug boo function
def boo():
    print("Boo has run!")