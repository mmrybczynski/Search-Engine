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
    print('''
    ██   ██ █████ ██     ██     ████████
    ██   ██ ██    ██     ██     ██    ██
    ██   ██ ██    ██     ██     ██    ██
    ███████ ████  ██     ██     ██    ██
    ██   ██ ██    ██     ██     ██    ██
    ██   ██ ██    ██     ██     ██    ██
    ██   ██ █████ ██████ ██████ ████████
    ''')
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

# Transform sql query to pandas dataframe
def postgresql_to_dataframe(conn, select_query, column_names):
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
   
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
   
    # We just need to turn it into a pandas dataframe
    database_df = pd.DataFrame(tupples, columns=column_names)
    return database_df

def main():
    system_info()
    clear_screen()
    print_center("# # # #  H E L L O  # # # #")
    print("Now you can chose dp you want to compare with files, which contains mpn's")
    compare_with_another_file = input("Do you want to compare with another file? [Y/N] ").upper()
    if compare_with_another_file == "Y":
        # Compare with file
        name_of_file = input("Name of file: ")
        file_df = pd.read_csv("csv-files/"+name_of_file+".csv") # Open file to compare
        file_df['name'] = file_df['name'].str.upper()
        compared_file = pd.merge(file_df['name'].reset_index(drop=True),phrases_df.reset_index(drop=True))

        print_center("# # # #  C O M P A R E D  F I L E  # # # #")
        print(compared_file)
    
    # Search name of company in phrases not found file
    name_of_manufacturer = input("Name of manufacturer: ").upper()
    search_name = phrases_df.loc[phrases_df['name'] == name_of_manufacturer]

    print_center("# # # #  O N L Y  N A M E  # # # #")
    print(search_name)

    # Combine database pandas dataframe with phrases not found



conn = connect(param_dic)
time.sleep(5)
phrases_df = pd.read_csv("csv-files/phrases-not-found.csv") # Open file with not found phrases
phrases_df['name']=phrases_df['name'].str.upper()
main()

# END of program
print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)