# Import libraries
import platform
import os
import time

# Print info about system
def system_info():
    print("Processor: "+platform.processor())
    print("System: "+platform.system()+" "+platform.release())

system_info()