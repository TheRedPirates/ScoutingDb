import os
import javaobj
import flask
import csv
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/createEntry', methods=['GET'])
def createEntry():
    objectbytes = request.args.get('object')
    pobj = javaobj.loads(bytearray.fromhex(objectbytes))
    entries = open(f"{pobj.userTeam}.csv", "a")
    if os.stat(f"{pobj.userTeam}.csv").st_size == 0:
        entries.write("userName,TeamNumber,GameNumber,b_defence,b_unsure,b_offence,AutoUpper,AutoLower,TeleUpper,TeleLower,Ranking,Notes,C1,C2,C3,C4\n")
    string = f"{pobj.userName},{pobj.TeamNumber},{pobj.GameNumber},{pobj.b_defence},{pobj.b_unsure},{pobj.b_offence},{pobj.AutoUpper},{pobj.AutoLower},{pobj.TeleUpper},{pobj.TeleLower},{pobj.Ranking},{pobj.Notes},{pobj.C1},{pobj.C2},{pobj.C3},{pobj.C4}\n"
    entries.write(string)
    entries.close()
    return "succsesfully created entry"
    
@app.route('/api/print', methods=['GET'])
def print():
    objectbytes = request.args.get('object')
    pobj = javaobj.loads(bytearray.fromhex(objectbytes))
    return str(dir(pobj))

app.run(host='127.0.0.1',port=80)

