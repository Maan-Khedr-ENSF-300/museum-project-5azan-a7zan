import sys
import time
import csv
import mysql.connector
from tabulate import tabulate
def connect(user_password):
    global cnx
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user='root',
        password= user_password)
    # Get a cursor
    global cur
    cur = cnx.cursor()

def read_sql(filepath):
    fd = open(filepath, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cur.execute(command)
        except:
            print("Command skipped: ", command)

def print_result():
    col_names=cur.column_names
    search_result=cur.fetchall()
    print("Search found ",len(search_result)," Entries:\n")
    search_result.insert(0, col_names)
    print(tabulate(search_result))

def identify_user(x,y):
    '''
    is able to identify which user 
    '''
    member_list=[]
    with open("member.csv","r") as folder:
        reader = csv.reader(folder,delimiter=',')
        for row in reader:
            items = dict(member=row[0], member_pass=row[1], authentication=row[2])
            member_list.append(items)
    #above code creates a list with the rows of the csv file as dictionaries
    for i in member_list:
        if (i.get('member') == x and i.get('member_pass') == y): #iterates over the list and checks if username and pass are valid.
            if (i.get('authentication') == 'admin'):
                return 1,member_list
            elif (i.get('authentication') == 'data_entry_users'):
                return 2,0
            elif (i.get('authentication') == 'end_user'):
                return 3,0
            elif (i.get('authentication') == 'blocked'):
                return 4,0
        else:
            continue
    return 0,0

def admin_interface(member_list):
    '''
    requires:   username
                password
                key: to unlock all the privilages
    promises:   user can:
                        Can add,edit,block users.  
                        Can make changes to databas
    ''' 
    while True:
        print("<<<<Menu>>>>\n1- add user\n2- edit user\n3- block user\n4- change database\n5- MySQL command line\n6- log out\n0- to exit")
        num = input("Please choose which option you want: ") 
        print("****Loading****");time.sleep(0.5) #visual effects
        if (num == '1'): #adds a user
            add_user(member_list)
        elif (num == '2'): #edits a user
            edit_user(member_list)
        elif (num == '3'): # blocks a user
            freska_block(member_list)
        elif (num == '4'): #change database
            data_entry_interface()
        elif (num == '5'):
            command = input('Please enter the MySQL command:')
            cur.execute(command)
            if 'select' in command.lower(): 
                print_result()
            cnx.commit()
            print("Command Executed");time.sleep(1)

        elif (num == '6'):
            main()
        elif (num == '0'):
            sys.exit() #forcibaly exits system (this is because all the code is in while loops)
        else:
            print("Choice invalid please re-enter");time.sleep(0.5)
            continue

def data_entry_users():
    '''
    requires:   username
                password
                key: to unlock all the privilages
    promises: user can:
                        add information tuples to the database 
                        modify existing information in the database
    '''
    while True:
        print("<<<<Menu>>>>\n1- add information\n2- Modify information\n3- log out")
        num = input("Please choose which option you want: ")
        print("****Loading****");time.sleep(0.5)
        if (num == '1'):
            insert_info() #add information
        elif (num == '2'):
            up_or_del() #edit information
        elif(num == '3'):
            main()
        else:
            print("Choice invalid please re-enter");time.sleep(0.5)
            continue

def end_user():
    '''
    requires:   name: username
                password
                key: to unlock all the privilages
    Can only lookup information
    '''
    while True:
        browsing_interface() #looks up information
        sel = input("press 0 to log out or enter to continue: ")
        if (sel == '0'):
            main()

def data_entry_interface():
    '''
    used to enter data into the database
    '''
    while True:
        print("<<<<menu>>>\n1- Lookup information\n2- Insert new tuples\n3- Update or delete tuples\n0- Exit program")
        menu = input("please enter number: ")
        print("****loading****");time.sleep(0.5)
        if (menu == '1'):
            browsing_interface()
        elif (menu == '2'):
            insert_info()
        elif (menu == '3'):
            up_or_del()
        elif (menu == '0'):
            sys.exit()
        else:
            print("invalid input please re-enter")
            continue


def add_user(x):
    '''
    requires: x = member list
    pryoussef
dds the data to the csv file
    '''
    while True:
        name = input("Please enter the username: ")
        password = input("Please enter the password: ")
        authentic = input("Please enter the authentication level (admin,data_entry_users,end_user): ")
        if not (authentic == 'admin' or authentic == 'data_entry_users' or authentic == 'end_user'):
            print("entered authentication is not valid, please re-enter")
            continue
        if (',' in name or ',' in password):
            print("There cannot be a ',' in the name or password, please re-enter")
            continue
        for i in x:
            if (i.get('member') == name and i.get('member_pass') == password):
                print("user already found, please re-enter")
                add_user(x)
        new_data = {'member':name, 'member_pass':password, 'authentication':authentic}
        x.append(new_data)
        print("****Loading****");time.sleep(0.5)
        with open("member.csv", 'w', newline="") as folder:
            writeCSV = csv.writer(folder, delimiter=',')
            for item in x:
                row = [item['member'], item['member_pass'],item['authentication']]
                writeCSV.writerow(row)
            print("User added successfully!\nGoing back to menu");time.sleep(0.5)
        admin_interface(x)
