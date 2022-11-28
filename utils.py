import os
import platform
import keyboard
import time

# Set console size
def setConSize(width,height):
    platformv = platform.system()
    if platformv == "Linux":
        #return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Darwin":
        #return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'mode con: cols={width} lines={height}') # Apply console size with windows.cmd.mode
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Set console title
def setConTitle(title):
    platformv = platform.system()
    if platformv == "Linux":
        return "\033[31mError: Platform Linux not supported yet!\033[0m"
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'title {title}') # Apply console size with windows.cmd.title
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Clear the screen
def clear():
    platformv = platform.system()
    if platformv == "Linux":
        return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system("CLS") # Apply console size with windows.cmd.cls
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"

# Pause
def pause():
    platformv = platform.system()
    if platformv == "Linux":
        return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Darwin":
        return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
            os.system("PAUSE > nul") # Apply console size with windows.cmd.cls
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"


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