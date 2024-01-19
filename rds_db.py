# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""

import pymysql
import encrypt as enc
import MySQLdb.cursors
#import aws_credentials as rds
# print("Username : "),
# username = input(),
# print("Password : "),
# password = input()
# conn = pymysql.connect(
#         host= 'd0018e-1.c38ei448gz7c.eu-north-1.rds.amazonaws.com', #endpoint link
#         port = 3306, # 3306
#         # user = username, # admin
#         # password = password, #adminadmin
#         db = 'D0018E1', #test

#         user = 'admin',
#         password = 'Potatis1'
#         )

#Table Creation
# cursor=conn.cursor()
# create_table="""
# create table Details (name varchar(200),email varchar(200),comment varchar(200),gender varchar(20) )
# """
# cursor.execute(create_table)

def select_all(mysql):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users')
    test = cur.fetchall()
    return test


def get_user(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM Users WHERE email = % s', (email,))
    test = cur.fetchone()
    return test
        

def insert_user(mysql,email, first_name, last_name, password, date_of_birth):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("INSERT INTO Users (email, first_name, last_name, password, date_of_birth) VALUES (%s,%s,%s,%s,%s)"
        ,(email, first_name, last_name, password, date_of_birth,))
    cur.commit()

    
def check_email(mysql,email):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT count(email) FROM Users WHERE email= %s", (email,))
    details = cur.fetchall()
    for elem in str(details):
        if elem == "0":
            return False
    return True
    
def check_credentails(mysql, email, password):
    if (get_user(mysql, email)) == 0:
        print("missing user")
        return False
    
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT password FROM Users WHERE email= %s", (email,))
    checkPass = cur.fetchall()
    # print("element", checkPass['password'])
    for element in checkPass:
        currentPass = element['password']
    return enc.decryptPassword(password, currentPass)