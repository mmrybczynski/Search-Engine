# Import libraries
import platform
import os
import time
import pandas as pd
import psycopg2
from colorama import Fore, Back, Style

# Connection to databse
param_dic = {
    "host"      :   "", # IP addres of postgres server
    "database"  :   "", # Name of database
    "user"      :   "", # User name
    "password"  :   "" # User password
}
def connect(params):
    conn = None
    try: # Try to connect to database
        print("\nConnecting to database")
        conn = psycopg2.connect(**params)
        print_center(Fore.GREEN+"Connection succesfull")
        print(Style.RESET_ALL)
    except (Exception,psycopg2.DatabaseError) as error: # Catch errors of connection
        print(Fore.RED+str(error))
        print(Style.RESET_ALL)
    return conn

# Print center function
def print_center(text):
    print(text.center(os.get_terminal_size().columns))

# Print info about system
def system_info():
    print("Processor: "+platform.processor())
    print("System: "+platform.system()+" "+platform.release()+"\n")
    time.sleep(3)

# Clear screen
def clear_screen():
    sys = str(platform.system()).upper()
    if sys == "WINDOWS":
        clear = lambda: os.system('cls')
        clear()
    else:
        clear = lambda: os.system('clear')
        clear()

def main():
    conn = connect(param_dic)
    system_info()
    phrases_df = pd.read_csv("phrases.csv") # Open file with not found phrases
    clear_screen()
    print_center("# # # #  H E L L O  # # # #")
    compare_with_another_file = input("\nDo you want to compare with another file? [Y/N] ").upper()
    if compare_with_another_file == "Y":
        name_of_file = input("Name: ")
        file_df = pd.read_csv(name_of_file+".csv") # Open file to compare
    else:
        print("Done")

main()