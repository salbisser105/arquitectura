from fileinput import filename
# from pyrebase import pyrebase
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request
import json
import http.client
from datetime import datetime

geoPosition = '95f541b868bc284aac25bb5401c73c1f'
baseUrl= 'http://api.positionstack.com/v1/forward'

import firebase_admin


firebaseConfig={
  'apiKey': "AIzaSyDneSkHdMLn8IzP86T_kCu6zHUSjGTFEYA",
  'authDomain': "arq-avanzada.firebaseapp.com",
  'databaseURL': "https://arq-avanzada-default-rtdb.firebaseio.com",
  'projectId': "arq-avanzada",
  'storageBucket': "arq-avanzada.appspot.com",
  'messagingSenderId': "153152091541",
  'appId': "1:153152091541:web:4bfd99be6a470011f0f29c"
}

# firebase = pyrebase.initialize_app(firebaseConfig)
# storage= firebase.storage()

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)

series_ref = db.collection('files')

#Listado  Funcionando
@app.route('/getFiles', methods=['GET'])
def get():
   # read data
  snapshots = list(db.collection(u'files').get())
  lista_archivos= [item.to_dict() for item in snapshots]
  return jsonify({"data":lista_archivos}),200


@app.route('/getPrediction', methods=['GET'])
def getPrediction():
  conn = http.client.HTTPSConnection("weatherbit-v1-mashape.p.rapidapi.com")
  payload = ''
  headers = {
    'X-RapidAPI-Host': 'weatherbit-v1-mashape.p.rapidapi.com',
    'X-RapidAPI-Key': '2829b312b3msh613b325399f4673p1a038djsn1b5ed4beb423'
  }
  args = request.args
  lon= args.get('lon')
  lat = args.get('lat')
  
  conn.request("GET", "/current?lon="+lon+"&lat="+lat, payload, headers)
  res = conn.getresponse()
  data = res.read().decode('utf-8')
  datajson= json.loads(data)
  testdata = datajson['data'][0]
  countryCode= testdata['country_code']
  cityName = testdata['city_name']
  temp = testdata['temp']
  currentDate = datetime.now()
  date= str(currentDate)
  data = {'pais':countryCode ,'ciudad':cityName, 'temp':temp}
  databd= {'pais':countryCode ,'ciudad':cityName, 'temp':temp, 'fecha': date, 'lon': lon, 'lat': lat}
  db.collection(u'predictions').add(databd)
  print(data)
  return jsonify(data)


@app.route('/sendDataset', methods=['POST'])
def send_data():
  if request.method == 'POST':
    f = request.files['file']
    filename = f.filename
    print(filename)
    # storage.child("archivos").put(filename)
    # url=storage.child("archivos").get_url(None)
    #storage.child("google.txt").download("","downloaded.txt")
  return jsonify((filename))

if __name__ == '__main__':
	app.run(debug=True)
