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


def edit_user(x):
    '''
    requires: x = member list
    promises: edits the data of a user in the csv file
    '''
    while True: 
        name = input("please input username you want to edit: ")
        for i in x: #checks if the user is registered
            if (i.get('member') == name):
                new_name = input("Please enter new username: ")
                new_password = input("Please enter new password: ")
                new_authentic = input("Please enter new authentication level: ")
                if not (new_authentic == 'admin' or new_authentic == 'data_entry_users' or new_authentic == 'end_user'):
                    print("entered authentication is not valid, please re-enter") #checks if the authentication is correct
                    edit_user(x)
                if (',' in new_name or ',' in new_password):
                    print("There cannot be a ',' in the name or password, please re-enter")
                    edit_user(x)
                i = 0
                while (i <= len(x)): #replaces the old user data with the new user data
                    if (x[i].get('member') == name ):
                        x[i]={'member':new_name, 'member_pass':new_password,'authentication':new_authentic}
                        i=i+1
                    i=i+1

                #line below puts the changes into the csv file
                with open("member.csv", 'w', newline="") as folder:
                    writeCSV = csv.writer(folder, delimiter=',')
                    for item in x:
                        row = [item['member'], item['member_pass'],item['authentication']]
                        writeCSV.writerow(row)
                print("User edited successfully!\nGoing back to menu");time.sleep(0.5)
                admin_interface(x)
        print("user not found, please re-enter")
        edit_user(x)


def freska_block(x):
    while True:

        name = input("please input username to block: ")
        for i in x: #checks if the user is registered
            if (i.get('member') == name):
                password = i.get('member_pass')
                k = 0
                while (k < len(x)): #makes the user into blocked status
                    if (x[k].get('member') == name ):
                        x[k]={'member':name, 'member_pass':password,'authentication':'blocked'}
                        k=k+1
                    k=k+1
                print("****Loading****");time.sleep(0.5)
                with open("member.csv", 'w', newline="") as folder:
                    writeCSV = csv.writer(folder, delimiter=',')
                    for item in x:
                        row = [item['member'], item['member_pass'],item['authentication']]
                        writeCSV.writerow(row)
                print("User blocked successfully!\nGoing back to menu");time.sleep(0.5)
                admin_interface(x)
        print("user not found, please re-enter")
        freska_block(x)

def insert_info():
    table = input("enter the name of the table to insert:")
    values = input("enter the values seperated by a comma: ")
    cur.execute(f"insert into {table} values ({values})")
    cnx.commit()
    print("info inserted")

def up_or_del():
    sel = input("Select 1 for update or 2 for delete: ")
    table = input("Select table to change: ")
    column  = input("Enter column name to search for the record: ")
    condition = input("Enter the search condition: ")
    if sel == "1":
        column1 = input("Select a coulumn to edit: ")
        value = input("Enter the new value: ")
        cur.execute(f"update {table} set {column1} = '{value}' where {column} = '{condition}' ")
        cnx.commit()
        print("info updated")
    elif sel == "2":
        cur.execute(f"delete from {table} where {column} = '{condition}' ")
        cnx.commit()
        print("info deleted")
    else:
        print("invalid selection")

def browsing_interface():
    '''
    promises: gets the information a user is looking for
    '''
    table = input("Select a table: ")
    column  = input("Enter column name to search for the record: ")
    condition = input("Enter the search condition: ")
    cur.execute(f"Select * from {table} where {column} = '{condition}' ")
    print_result()

def startup():
    print("<<<<System Start Up>>>>");time.sleep(1)
    connect(input("Please enter the root database password: "))
    if(input("do you want to create/reset the database (y or n): ") == "y"):
        read_sql('ART_Database.sql')
        print("Database has been created/reseted successfully");time.sleep(1)
        
    else:
        print("Database wasn't created/reseted");time.sleep(1)

def main():
    cur.execute("USE ARTGALLERY")
    while True:
        username = input("Please enter username (Enter: admin, data_entry or guest): ")
        password = input("Please enter password (Enter: admin_password, data_entry_password or guest_password): ")
        code,member_list = identify_user(username, password)
        if (code == 1):
            print(f"<<<<Welcome {username}, loading up menu>>>>");time.sleep(0.5)
            admin_interface(member_list)
        elif (code == 2):
            print(f"<<<<Welcome {username}, loading up menu>>>>");time.sleep(0.5)
            data_entry_users()
        elif (code == 3):
            print(f"<<<<Welcome {username}, Which information are you looking for today?>>>>");time.sleep(0.5)
            end_user()
        elif (code == 4):
            print(f"user {username} is blocked exiting program");time.sleep(0.5)
            sys.exit()
        else:
            print("User not found, Please re-enter credentials")
            continue

if __name__ == '__main__':
    startup()
    main()