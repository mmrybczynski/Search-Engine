# Import libraries
import platform
import os
import time

# Print center function
def print_center(text):
    print(text.center(os.get_terminal_size().columns))

# Print info about system
def system_info():
    print("\nProcessor: "+platform.processor())
    print("System: "+platform.system()+" "+platform.release()+"\n")
    time.sleep(3)

# Clear screen
def clear_screen():
    sys = str(platform.system()).upper()
    system_info()
    if sys == "WINDOWS":
        clear = lambda: os.system('cls')
        clear()
    else:
        clear = lambda: os.system('clear')
        clear()

def main():
    clear_screen()
    print_center("\n# # # #  H E L L O  # # # #\n")

main()