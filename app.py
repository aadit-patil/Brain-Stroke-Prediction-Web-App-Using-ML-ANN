from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymysql
import joblib
import os
import  numpy as np
import pickle


app= Flask(__name__)
app.secret_key = os.urandom(24)
mysql= MySQL()

#MySQL configuration
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='stroke_prediction_system'

mysql.init_app(app)

global userID
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/register",methods=['POST','GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_data WHERE username = % s', (username))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user_data VALUES (% s, % s, % s)', (name,username, password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)


@app.route("/loginCheck",methods=['POST','GET'])
def loginCheck():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_data WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('strokeCheck.html')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)
@app.route("/strokeCheck")
def strokeCheck():
    render_template("strokeCheck.html")

@app.route("/signupCheck")
def signupCheck():
    print("Hello New User")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/result",methods=['POST','GET'])
def result():
    gender=int(request.form['gender'])
    age=int(request.form['age'])
    hypertension=int(request.form['hypertension'])
    heart_disease = int(request.form['heart_disease'])
    ever_married = int(request.form['ever_married'])
    work_type = int(request.form['work_type'])
    Residence_type = int(request.form['Residence_type'])
    avg_glucose_level = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    smoking_status = int(request.form['smoking_status'])

    x=np.array([gender,age,hypertension,heart_disease,ever_married,work_type,Residence_type,
                avg_glucose_level,bmi,smoking_status]).reshape(1,-1)

    scaler_path=os.path.join('/home/aadit/project/Stroke-Risk-Prediction-using-Machine-Learning-master','models/scaler.pkl')
    scaler=None
    with open(scaler_path,'rb') as scaler_file:
        scaler=pickle.load(scaler_file)

    x=scaler.transform(x)

    model_path=os.path.join('/home/aadit/project/Stroke-Risk-Prediction-using-Machine-Learning-master','models/dt.sav')
    dt=joblib.load(model_path)

    Y_pred=dt.predict(x)

    #inserting in prediction history
    username=session['username']
    username=str(username)
    pred=str(Y_pred[0])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('insert into preds values(% s,% s)', (username,pred))
    mysql.connection.commit()
   

    # for No Stroke Risk
    if Y_pred==0:
        return render_template('nostroke.html')
    else:
        return render_template('stroke.html')

@app.route("/pastResult")
def pastResult():
    print("showing past result")
    username=session['username']
    username=str(username)
    cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor2.execute('SELECT * FROM preds WHERE uname = % s', [username])
    data = cursor2.fetchall()
    print(data)
    return render_template('ppreds.html',data=data,uname=username)

if __name__=="__main__":
    app.run(debug=True,port=7384)