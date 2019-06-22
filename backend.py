from flask import Flask, render_template, flash, redirect, request, session, abort
import random
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)
ok='noSuccess'
emri=""
ditelindja=''
vendlindja=''
vendbanimi=''

def success():
    global ok
    ok="Success"
def nosuccess():
    global ok
    ok="NoSuccess"

def connect(para, password):
    try:
        conn=mysql.connector.connect(host='localhost', database='python', user='frankoprifti', password='franko1998')
        if conn.is_connected():
            print('MySql Connected!')
            query=conn.cursor()
            query.execute("SELECT password FROM admins WHERE username='%s'"%(para))
            rows=query.fetchall()
            for row in rows:
                if row[0]==password:
                    print('success')
                    success()
                else:
                    print('not success')
                    nosuccess()


            
    except Error as e:
        print(e)
    finally:
        conn.close()
def getName(name):
    try:
        conn=mysql.connector.connect(host='localhost', database='python', user='frankoprifti', password='franko1998')
        if conn.is_connected():
            global emri
            global ditelindja
            global vendlindja
            global vendbanimi
            query=conn.cursor()
            query.execute("SELECT * FROM admins WHERE username='%s'"%(name))
            rows=query.fetchall()
            for row in rows:
                emri=row[2]
                ditelindja=row[3]
                vendlindja=row[4]
                vendbanimi=row[5]
                
    except Error as e:
        print(e)
    finally:
        conn.close()
                    

@app.route("/")
def main():
    alert='Login'
    return render_template('index.html', **locals())
@app.route("/home", methods=['POST'])
def home():
    name=request.form['name']
    password=request.form['password']
    connect(name,password)
    if ok == "Success":
        getName(name)
        global emri
        details = {
            "name": emri,
            "username": name,
            "ditelindja": ditelindja,
            "vendlindja": vendlindja,
            "vendbanimi": vendbanimi
        }
        return render_template('home.html', **locals())
    else:
        alert='Your Credentials Are Not Correct'
        return render_template('index.html', **locals())
        

@app.route("/register") 
def register():
    return render_template('register.html')

def addUser(username, password, name, birthday, birthplace, living) :
    try:
        conn=mysql.connector.connect(host='localhost', database='python', user='frankoprifti', password='franko1998')
        if conn.is_connected():
            query=conn.cursor()
            sql="INSERT INTO admins(username, password, emri, ditelindja, vendlindja,vendbanimi) VALUES(%s,%s,%s,%s,%s,%s)"
            values=(username, password, name, birthday, birthplace, living)
            query.execute(sql,values)
            conn.commit()
            print(query.rowcount)

            
    except Error as e:
        print(e)
    finally:
        conn.close()

@app.route("/user", methods=['POST'])
def user():
    
    username=request.form['username']
    password=request.form['password']
    name=request.form['name']
    birthday=request.form['birthday']
    birthplace=request.form['birthplace']
    living=request.form['living']
    addUser(username,password,name,birthday,birthplace,living)
    alert='Login'
    return render_template('index.html',**locals())

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=81)