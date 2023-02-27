# Import libraries
import platform
import os
import time
import pandas as pd
import psycopg2
from colorama import Fore, Back, Style
import warnings
from pick import pick
warnings.simplefilter(action='ignore', category=FutureWarning)

# Connection to databse
param_dic = {
    "host"      :   "localhost", # IP addres of postgres server
    "database"  :   "dataset", # Name of database
    "user"      :   "mati", # User name
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
    print("Do you have file with mpns to compare")
    compare_with_another_file = input("[Y/N] ").upper()
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
    if not conn == None:
        temp = "'"+name_of_manufacturer+"'"
        # connect to database
        column_names = ["mpn", "manufacturer_root_name"]

        # Here we can tyoe SQL query
        query =     """SELECT mpn,manufacturer_root_name 
                    FROM manufacturers
                    WHERE manufacturer_root_name ILIKE""" + temp

        query_df = postgresql_to_dataframe(conn, query, column_names)
        query_df['mpn']=query_df['mpn'].str.upper()
        new_name = query_df.rename(columns={'mpn':'name'})
        founded_in_database = pd.merge(phrases_df.reset_index(drop=True),new_name['name'].reset_index(drop=True))
        print("")
        print_center("# # # #  D A T A B A S E  # # # #")
        print(founded_in_database)
    
    # Look similar phrases
    array_to_checking = [name_of_manufacturer+" ",name_of_manufacturer+":",name_of_manufacturer+"-",name_of_manufacturer+"."]
    similar_phrases = phrases_df.loc[phrases_df['name'].str.contains('|'.join(array_to_checking)).ffill(False)]
    print("")
    print_center("# # # #  S I M I L A R # # # #")
    print(similar_phrases)
    print("")

for i in range(os.get_terminal_size().columns-1):
    if i >= os.get_terminal_size().columns-2:
        print("#")
    else:
        print("#",end="")

title = 'Please choose what do you want to do'
options = ['Compare two files', 'Check mpn', 'Check qty of search company', 'Check qty of search company for more companys']
option, index = pick(options, title, indicator='=>', default_index=2)

if index == 0: # Compare two files
    compareTwoFiles()
elif index == 1:
    checkMPN()
elif index == 2:
    searchForOneCompany()
elif index == 3:
    searchForMore()
else:
    # END of program
    print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)

conn = connect(param_dic)
time.sleep(5)
phrases_df = pd.read_csv("csv-files/phrases-not-found.csv") # Open file with not found phrases
phrases_df['name']=phrases_df['name'].str.upper()
main()

# END of program
print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)