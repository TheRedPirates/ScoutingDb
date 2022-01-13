import javaobj
import flask
import json
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

@app.route('/')
def home():
  return "I'm alive"


@app.route('/api/createEntry', methods=['GET'])
def createEntry():
    objectbytes = request.args.get('object')
    pobj = javaobj.loads(bytearray.fromhex(objectbytes))
    with open("entries.json") as fp:
        entries = json.load(fp)
    entries.append({
        "TeamNumber":pobj.TeamNumber,
        "GameNumber":pobj.GameNumber,
        "b_defence":pobj.b_defence,
        "b_unsure":pobj.b_unsure,
        "b_offence":pobj.b_offence,
        "AutoUpper":pobj.AutoUpper,
        "AutoLower":pobj.AutoLower,
        "TeleUpper":pobj.TeleUpper,
        "TeleLower":pobj.TeleUpper,
        "Ranking":pobj.Ranking,
        "Notes":pobj.Notes,
        "Climbing1":pobj.Climbing[0],
        "Climbing2":pobj.Climbing[1],
        "Climbing3":pobj.Climbing[2],
        "Climbing4":pobj.Climbing[3],
    })
    with open("entries.json", 'w') as json_file:
        json.dump(entries, json_file, indent=4,separators=(',',': '))
    return "succsesfully created entry"
    
@app.route('/api/print', methods=['GET'])
def print():
    objectbytes = request.args.get('object')
    pobj = javaobj.loads(bytearray.fromhex(objectbytes))
    return str(dir(pobj))

def get_username(username):
  with open('usernames.txt', 'r') as usernamefile:
    line = usernamefile.read()
    if username == str(line) or username in str(line) or username == str(line).split(' ') or username == str(line).split('\n'):
      return True
    else:
      return False

def create_account(username):
  with open('usernames.txt', 'a') as usernamefile:
    if username in usernamefile.read():
      usernamefile.write(' '+str(username))
      return True
    else:
      return False

class Quotes(Resource):
  def get(self, quote_type):
    return get_quotes(quote_type)

class Username(Resource):
  def get(self, username):
    return get_username(username)

class CreateAccount(Resource):
    def get(self, username):
      return create_account(username)

class Facts(Resource):
  def get(self, fact_type):
    return get_facts(fact_type)

  

#api.add_resource(Test, '/api/restful')
api.add_resource(Quotes, '/api/quotes/<string:quote_type>')
api.add_resource(Facts, '/api/facts/<string:fact_type>')
api.add_resource(Username,'/api/username/<string:username>')
api.add_resource(CreateAccount,'/api/createaccount/<string:username>')

  
app.run(host='127.0.0.1',port=80)

