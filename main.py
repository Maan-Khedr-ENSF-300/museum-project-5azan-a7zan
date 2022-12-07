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