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

def searchForOneCompany():
    conn = connect(param_dic)
    time.sleep(3)
    print_center("# # # #  H E L L O  # # # #")
    year = input("Year of phrases not found file: ")
    phrases_df = pd.read_csv("csv-files/phrases-not-found-"+year+".csv") # Open file with not found phrases
    phrases_df['name']=phrases_df['name'].str.upper()
    print("Do you have file with mpns to compare [Y/N]")
    compare_with_another_file = input(">>> ").upper()
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

    # Close connection with database
    conn.close()

    # END of program
    print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)

def tempSearch(manufacturer_name,phrases_df,conn):
    # Search name of company in phrases not found file
    print_center('# # # #  '+manufacturer_name+'  # # # #')
    search_name = phrases_df.loc[phrases_df['name'] == manufacturer_name]
    print(search_name)

    # Combine database pandas dataframe with phrases not found
    if not conn == None:
        temp = "'"+manufacturer_name+"'"
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
        if len(founded_in_database) > 0:
            print_center("# # # #  D A T A B A S E  # # # #")
            print(founded_in_database)

    # Look similar phrases
    array_to_checking = [manufacturer_name+" ",manufacturer_name+":",manufacturer_name+"-",manufacturer_name+"."]
    similar_phrases = phrases_df.loc[phrases_df['name'].str.contains('|'.join(array_to_checking)).ffill(False)]
    print("")
    if len(similar_phrases) > 0:
        print_center("# # # #  S I M I L A R # # # #")
        print(similar_phrases)
        print("")

def searchForMoreCompanies():
    conn = connect(param_dic)
    time.sleep(3)
    print_center("# # # #  H E L L O  # # # #")
    year = input("Year of phrases not found file: ")
    phrases_df = pd.read_csv("csv-files/phrases-not-found-"+year+".csv") # Open file with not found phrases
    phrases_df['name']=phrases_df['name'].str.upper()

    typing = True
    names_list = []
    while(typing == True):
        name = input("Name: ").upper()
        if not name == "":
            names_list.append(name)
        else:
            typing = False

    for i in range(len(names_list)):
        tempSearch(names_list[i],phrases_df,conn)

    # Close connection with database
    conn.close()

    # END of program
    print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)

def checkMPN():
    conn = connect(param_dic)
    time.sleep(3)

    mpn = input("MPN: ")

    if not conn == None:
        temp = "'"+mpn+"'"
        # connect to database
        column_names = ["mpn", "manufacturer_root_name"]

        # Here we can tyoe SQL query
        query =     """SELECT mpn,manufacturer_root_name 
                    FROM manufacturers
                    WHERE mpn ILIKE""" + temp

        query_df = postgresql_to_dataframe(conn, query, column_names)
        print("")
        print_center("# # # #  M P N  # # # #")
        print(query_df)

        # Close connection with database
        conn.close()

def compareTwoFiles():
    # Type name of files to open
    firstFile = input("Name of first file: ")
    secondFile = input("Name of second file: ")

    first_df = pd.read_csv('files/'+firstFile+'.csv')
    second_df = pd.read_csv('files/'+secondFile+'.csv')

    # Show columns name and type column to compare
    print("\nColumns in first file:",end=" ")
    for col in first_df.columns:
        print(col, end=" | ")
    print("")
    column_first_file = input("Which column do you want to compare? ")

    print("\nColumns in second file:",end=" ")
    for col in second_df.columns:
        print(col, end=" | ")
    print("")
    column_second_file = input("Which column do you want to compare? ")

    # Rename columns
    first_new_df = first_df.rename(columns={column_first_file:'Compared'})
    second_new_def = second_df.rename(columns={column_second_file:'Compared'})

    # Normalized values to upper letters
    first_new_df['Compared'] = first_new_df['Compared'].str.upper()
    second_new_def['Compared'] = second_new_def['Compared'].str.upper()

    # Merge files
    merged_df = pd.merge(first_new_df['Compared'].reset_index(drop=True),second_new_def['Compared'].reset_index(drop=True))
    print(merged_df)
    print("")

    # END of program
    print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)

def checkDistributor():
    file_with_distributors = pd.read_csv("csv-files/distributors.csv") # Open file with distributors
    file_with_distributors['name'] = file_with_distributors['name'].str.upper()
    name_of_manufacturer = input("Type name of manufacturer: ").upper()
    print_center("# # # #  N A M E  # # # #")
    name = file_with_distributors.loc[file_with_distributors['name']== name_of_manufacturer]
    print(name)
    print_center("# # # #  S I M I L L A R  # # # #")
    simillar_name = file_with_distributors.loc[file_with_distributors['name'].str.contains(name_of_manufacturer)]
    print(simillar_name)

system_info()
clear_screen()

title = 'Please choose what do you want to do'
options = ['Check qty of search company (One year)','Check qty of search company (Two years)','Check qty of search company for more companies (One year)','Check qty of search company for more companies (Two year)','Compare two files', 'Check mpn', 'Check distributors']
option, index = pick(options, title, indicator='=>', default_index=1)

if index == 0: # Check qty of search company (One year)
    searchForOneCompany()
elif index == 1: # Check qty of search company (Two years)
    print("")
elif index == 2: # Check qty of search company for more companies (One year)
    searchForMoreCompanies()
    print("")
elif index == 3: # Check qty of search company for more companies (Two year)
    print("")
elif index == 4: # Compare two files'
    compareTwoFiles()
elif index == 5: # Check mpn
    checkMPN()
elif index == 6:
    checkDistributor()
else:
    # END of program
    print_center(Back.GREEN+"# # # #  D O N E  # # # #"+Style.RESET_ALL)