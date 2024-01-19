import pymysql
#import aws_credentials as rds

def connect_db(user,password):
    conn = pymysql.connect(
            host= 'd0018e-1.c38ei448gz7c.eu-north-1.rds.amazonaws.com', #endpoint link
            port = 3306, # 3306
            user = user, # admin
            password = password, #
            db = 'D0018E1', #test
            
            # user = 'customer',
            # password = 'customer'
            )
    return conn

def insert_details(conn, name,email,comment,gender):
    cur=conn.cursor()
    cur.execute("INSERT INTO Details (name,email,comment,gender) VALUES (%s,%s,%s,%s)", (name,email,comment,gender))
    conn.commit()

def get_details(conn):
    cur=conn.cursor()
    cur.execute("SELECT * FROM Details")
    details = cur.fetchall()
    return details




