import secrets
import javaobj
import csv
import flask
from flask import render_template, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register')
def register():
    teamtoken = secrets.token_urlsafe(16)
    with open(f"/TeamData/{teamtoken}.csv",'w') as file:
        file.write("Alias,TeamNumber,GameNumber,b_defence,b_unsure,b_offence,AutoUpper,AutoLower,TeleUpper,TeleLower,Ranking,Notes,C1,C2,C3,C4\n")
    with open("secrets",'a') as secretfile:
        secretfile.write(f"{request.args.get('TeamNumber')}:{teamtoken}")
    return f"""
        Successfully registered team,
        Please save and use this token in your login credentials on our mobile app:
        {teamtoken}
        """

@app.route('/api/login')
def login():
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
    entries = open(f"/TeamData/{pobj.Token}.csv", "a")
    string = f"{pobj.Alias},{pobj.TeamNumber},{pobj.GameNumber},{pobj.b_defence},{pobj.b_unsure},{pobj.b_offence},{pobj.AutoUpper},{pobj.AutoLower},{pobj.TeleUpper},{pobj.TeleLower},{pobj.Ranking},{pobj.Notes},{pobj.C1},{pobj.C2},{pobj.C3},{pobj.C4}\n"
    entries.write(string)
    entries.close()
    return "succsesfully created entry"

app.run(host="0.0.0.0",port=5000)

