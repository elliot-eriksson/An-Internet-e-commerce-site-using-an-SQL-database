# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:34:18 2020

@author: hp
"""

import pymysql
#import aws_credentials as rds
conn = pymysql.connect(
        host= 'd0018e-1.c38ei448gz7c.eu-north-1.rds.amazonaws.com', #endpoint link
        port = 3306, # 3306
        user ='admin', # admin
        password = 'Potatis1', #adminadmin
        db = 'D0018E1', #test
        
        # user = 'customer',
        # password = 'customer'
        )

#Table Creation
# cursor=conn.cursor()
# create_table="""
# create table Details (name varchar(200),email varchar(200),comment varchar(200),gender varchar(20) )
# """
# cursor.execute(create_table)



def insert_details(name,email,comment,gender):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name,email,comment,gender))
    conn.commit()

def get_details():
    cur=conn.cursor()
    cur.execute("SELECT * FROM Details")
    details = cur.fetchall()
    return details

def insert_user(email, firstName, lastName, password, dateOfBirth):
    cur=conn.cursor()
    cur.execute("INSERT INTO Users (email, firstName, lastName, password, dateOfBirth, dateLastPurchase) VALUES (%s,%s,%s,%s,%s)"
        ,(email, firstName, lastName, password, dateOfBirth))
    conn.commit()
    
def get_user(email):
    cur=conn.cursor()
    cur.execute("SELECT count(email) FROM Users WHERE email= %s", (email))
    details = cur.fetchall()
    return details
    

    