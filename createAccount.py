import sys
import os
import pymysql

current_dir = os.path.dirname(os.path.realpath(__file__))

parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from connect import connect_db

def insert_user(conn, email, first_name, last_name, password, date_of_birth, date_last_purchase):
    cur=conn.cursor()
    cur.execute("INSERT INTO Users (email, first_name, last_name, password, date_of_birth, date_last_purchase) VALUES (%s,%s,%s,%s,%s,%s,)"
        ,(email, first_name, last_name, password, date_of_birth, date_last_purchase))
    conn.commit()


def get_user(conn,email):
    cur=conn.cursor()
    cur.execute("SELECT count(email) FROM Users WHERE email= %s", (email))
    details = cur.fetchall()
    for elem in details:
        if elem == 0:
            return 0
    return details

def main():
    #Create database connection for init user
    user = "customer"
    login = "customer"

    conn = connect_db

