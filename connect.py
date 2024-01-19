import pymysql
#import aws_credentials as rds
conn = pymysql.connect(
        host= 'd0018e-1.c38ei448gz7c.eu-north-1.rds.amazonaws.com', #endpoint link
        port = 3306, # 3306
        user ='admin', # admin
        password = '', #
        db = 'D0018E1', #test
        
        # user = 'customer',
        # password = 'customer'
        )

def insert_details(name,email,comment,gender):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name,email,comment,gender))
    conn.commit()

def get_details():
    cur=conn.cursor()
    cur.execute("SELECT * FROM Details")
    details = cur.fetchall()
    return details

def insert_user(email, firstName, lastName, password, dateOfBirth, dateLastPurchase):
    cur=conn.cursor()
    cur.execute("INSERT INTO Users (email, firstName, lastName, password, dateOfBirth, dateLastPurchase) VALUES (%s,%s,%s,%s,%s,%s,)"
        ,(email, firstName, lastName, password, dateOfBirth, dateLastPurchase))
    conn.commit()
    
def get_user(email):
    cur=conn.cursor()
    cur.execute("SELECT count(email) FROM Users WHERE email= %s", (email))
    details = cur.fetchall()
    return details




