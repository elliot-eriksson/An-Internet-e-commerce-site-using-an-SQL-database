from flask import Flask, render_template, request, flash, redirect,url_for, jsonify, session 
from flask import Response,send_file

app = Flask(__name__)

import rds_db as db

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/insert',methods = ['post'])
def insert():
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['optradio']
        comment = request.form['comment']
        db.insert_details(name,email,comment,gender)
        details = db.get_details()
        print(details)
        for detail in details:
            var = detail
        return render_template('index.html',var=var)

@app.route('/insert new customer',methods = ['post'])
def insert_new_user():
    if request.method == 'Post':
        email = request.form['email']
        if db.get_user(email) != 0:
            var = "Email in use"
            return render_template('index.html', var=var)
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        dateOfBirth = request.form['dateOfBirth']
        db.insert_user(email,firstName,lastName,password,dateOfBirth)
        var = "User created"
        return render_template('index.html', var=var)

if __name__ == "__main__":
    
    app.run(debug=True)