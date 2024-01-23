from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import rds_db as db
import encrypt as enc

app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'd0018e-1.c38ei448gz7c.eu-north-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'Customer'
print("Password")
userpass = input()
app.config['MYSQL_PASSWORD'] = userpass
app.config['MYSQL_DB'] = 'D0018E1'

mysql = MySQL(app)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/login')
# @app.route('/login.html')
def loginPage():
    return render_template('login.html')
@app.route('/l')
def reginPage():
    return render_template('create_user.html')


@app.route('/users')
def selectUsers():
    try:
        if session['isAdmin']:
            userDetails = db.select_all(mysql)
    # print(userDetails)
        for e in userDetails:
            print(e['customer_id'])
        return render_template('admin.html', userDetails=userDetails)
    except:
        var = "Access Denied"
        return render_template('index.html', var=var)


@app.route('/insert new customer',methods = ['post'])
def insert_new_user():
    if request.method == 'POST':
        email = request.form['email']
        if db.check_email(mysql, email):
            var = "Email in use"
            return render_template('index.html', var=var)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = enc.encrypPassword(request.form['password'])
        # password = request.form['password']
        date_of_birth = request.form['date_of_birth']
        db.insert_user(mysql,email,first_name,last_name,password, date_of_birth)
        var = "User created"
        return render_template('index.html', var=var)
#TODO Implement what will happen when you loggin 
# Store the customer_id  
@app.route('/login',methods = ['post'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        # password = request.form['pwd']
        password = request.form['pwd']

        if email == "admin":
            app.config['MYSQL_USER'] = 'admin'
            app.config['MYSQL_PASSWORD'] = password
            var = "admin"
            session['loggedin'] = True
            session['isAdmin'] = True
            return render_template('admin.html', var=var)

        if db.check_credentails(mysql,email, password):
            account = db.get_user(mysql,email)

            # cursor = conn.cursor()
            # cursor.execute('SELECT * FROM accounts WHERE email = % s', (email))
            if account:
                # print("account", account)
                session['loggedin'] = True
                session['id'] = account['customer_id']
                session['username'] = account['email']
                # print("acount", account['customer_id'])
            
            var = session['id']

            return render_template('index.html', var=var)
    var = "Account error"
    return render_template('index.html', var=var)

@app.route('/logout')
def logout():
    if session['isAdmin']:
        app.config['MYSQL_USER'] = 'Customer'
        app.config['MYSQL_PASSWORD'] = userpass
        session.pop('isAdmin', False)
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(port=5002, debug=True)
