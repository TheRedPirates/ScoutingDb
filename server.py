import secrets
import javaobj
import csv
import flask
import os

from flask import render_template, request, session, redirect
from flask_session import Session


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@app.route('/index')
def Index():
    return render_template("index.html")

@app.route('/PrivacyPolicy')
def PrivacyPolicy():
    return render_template("privacyPolicy.html")

@app.route('/register', methods=['POST','GET'])
def Register():
    if request.method == "POST":
        if session.get("token"):
            return render_template("alreadyRegistered.html",token=session.get("token"))
        
        teamtoken = secrets.token_urlsafe(16)
        with open("secrets",'a') as secretfile:
            secretfile.write(f"{request.form.get('TeamNumber')}:{teamtoken}\n")
        
        os.chdir(r'TeamData')
    
        with open(f"{teamtoken}.csv",'w') as file:
            file.write("Alias,TeamNumber,GameNumber,b_defence,b_unsure,b_offence,AutoUpper,AutoLower,TeleUpper,TeleLower,Ranking,Notes,C1,C2,C3,C4\n")
        
        os.chdir('..')

        session["token"] = teamtoken
        return render_template("successMessage.html",token=teamtoken)

    return render_template("index.html") 
@app.route('/api/login')
def Login():
    with open("secrets",'r') as secretfile:
        for line in secretfile:
            line = line.strip().split(':')
            if line[1] == request.args.get('token'):
                return line[0]
        return "False"
            

@app.route('/api/createEntry', methods=['GET'])
def createEntry():
    objectbytes = request.args.get('object')
    pobj = javaobj.loads(bytearray.fromhex(objectbytes))

    os.chdir(r'TeamData')
    
    entries = open(f"{pobj.Token}.csv", "a")
    string = f"{pobj.Alias},{pobj.TeamNumber},{pobj.GameNumber},{pobj.b_defence},{pobj.b_unsure},{pobj.b_offence},{pobj.AutoUpper},{pobj.AutoLower},{pobj.TeleUpper},{pobj.TeleLower},{pobj.Ranking},{pobj.Notes},{pobj.C1},{pobj.C2},{pobj.C3},{pobj.C4}\n"
    entries.write(string)
    entries.close()
    
    os.chdir('..')
    
    return "succsesfully created entry"

app.run(host="0.0.0.0",port=5000)

