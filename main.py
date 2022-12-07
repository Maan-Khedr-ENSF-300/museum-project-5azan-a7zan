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