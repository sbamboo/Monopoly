# ConUtils: Console utility functions for python, Obs! xterm needed on linux 
# Made by: Simon Kalmi Claesson and modified to work with crosshell
# Version: 1.2

# [Imports]
import os
import platform
import time
import sys

# Console size (Curses)
def _setConSize_curses(width,height):
    '''INTERNAL, gets the consoleSize using curses.'''
    try: import curses
    except:
        os.system(f"{sys.executable} -m pip install curses")
        import curses
    try:
        stdscr = curses.initscr()
        curses.resizeterm(height, width)
    finally:
        curses.endwin()

# Set console size
def setConSize(width,height):
    '''Sets the console size on supported terminals (both inputs must be int)
    ConUtils is dependent on platform commands so this might not work everywere :/'''
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"resize -s {height} {width}")
    # Darwin using resize
    elif platformv == "Darwin":
        #os.system(f"resize -s {height} {width}")
        _setConSize_curses(width,height)
    # mode for windows
    elif platformv == "Windows":
        os.system(f'mode con: cols={width} lines={height}')
    # Error message if platform isn't supported
    else:
        raise Exception(f"Error: Platform {platformv} not supported yet!")

# Set console title
def setConTitle(title):
    '''Sets the console title on supported terminals (Input as string)
    ConUtils is dependent on platform commands so this might not work everywere :/'''
    # Get platform
    platformv = platform.system()
    # Linux using ANSI codes
    if platformv == "Linux":
        sys.stdout.write(f"\x1b]2;{title}\x07")
    # Mac not supported
    elif platformv == "Darwin":
        sys.stdout.write(f"\x1b]2;{title}\x07")
    # Windows using the title command
    elif platformv == "Windows":
        os.system(f'title {title}')
    # Error message if platform isn't supported
    else:
        raise Exception(f"Error: Platform {platformv} not supported yet!")

# Clear the screen
def clear():
    '''Attempts to clear the screen.
    ConUtils is dependent on platform commands so this might not work everywere :/'''
    # Get platform
    platformv = platform.system()
    # Linux using clear
    if platformv == "Linux":
        os.system("clear")
    # Mac using clear
    elif platformv == "Darwin":
        os.system(f"clear")
    # Windows using cls
    elif platformv == "Windows":
        os.system("CLS")
    # Error message if platform isn't supported
    else:
        raise Exception(f"Error: Platform {platformv} not supported yet!")

# Pause
def pause():
    '''Pauses the terminal (Waits for input)
    ConUtils is dependent on platform commands so this might not work everywere :/'''
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        os.system(f"read -p ''")
    # Mac using resize
    elif platformv == "Darwin":
        os.system(f"read -n 1 -s -r -p ''")
    # Windows using PAUSE
    elif platformv == "Windows":
        os.system("PAUSE > nul")
    # Error message if platform isn't supported
    else:
        raise Exception(f"Error: Platform {platformv} not supported yet!")

# Debug boo function
def boo():
    '''Smal testing function to execute a print statement.'''
    print("Boo! Oh now you are scared :)")

# Dummy function (call a dummy dummy to protect my yumme yummy tummy tummy)
def dummy():
    '''Smal testing function that does nothing'''
    pass

# Os checker functions
def IsWindows() -> bool:
    '''Checks if the platform name is Windows'''
    # Get platform and return boolean value depending of platform
    platformv = platform.system()
    if platformv == "Linux":
        return False
    elif platformv == "Darwin":
        return False
    elif platformv == "Windows":
        return True
    else:
        return False
def IsLinux() -> bool:
    '''Checks if the platform name is Linux'''
    # Get platform and return boolean value depending of platform
    platformv = platform.system()
    if platformv == "Linux":
        return True
    elif platformv == "Darwin":
        return False
    elif platformv == "Windows":
        return False
    else:
        return False
def IsMacOS() -> bool:
    '''Checks if the platform name is Darwin (Is Mac)'''
    # Get platform and return boolean value depending of platform
    platformv = platform.system()
    if platformv == "Linux":
        return False
    elif platformv == "Darwin":
        return True
    elif platformv == "Windows":
        return False
    else:
        return False