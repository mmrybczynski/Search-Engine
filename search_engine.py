# Import libraries
import platform
import os
import time

# Print info about system
def system_info():
    print("Processor: "+platform.processor())
    print("System: "+platform.system()+" "+platform.release())
    time.sleep(3)

def clear_screen():
    sys = str(platform.system()).upper()
    system_info()
    if sys == "WINDOWS":
        clear = lambda: os.system('cls')
        clear()
    else:
        clear = lambda: os.system('clear')
        clear()

clear_screen()