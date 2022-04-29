from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, jsonify, request
import json
import requests
import http.client

geoPosition = '95f541b868bc284aac25bb5401c73c1f'
baseUrl= 'http://api.positionstack.com/v1/forward'

# from models import Series

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("clave.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
series_ref = db.collection('files')

firebaseConfig={
  'apiKey': "AIzaSyDneSkHdMLn8IzP86T_kCu6zHUSjGTFEYA",
  'authDomain': "arq-avanzada.firebaseapp.com",
  'databaseURL': "https://arq-avanzada-default-rtdb.firebaseio.com",
  'projectId': "arq-avanzada",
  'storageBucket': "arq-avanzada.appspot.com",
  'messagingSenderId': "153152091541",
  'appId': "1:153152091541:web:4bfd99be6a470011f0f29c"
}
app = Flask(__name__)

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
  data = {'pais':countryCode ,'ciudad':cityName, 'temp':temp}
  db.collection(u'predictions').add(data)
  return jsonify(data)


@app.route('/sendDataset', methods=['POST'])
def send_data():
  db.collection(u'files').add({'name':'Test','url':'www.test1.com','type':'csv'})
  return 'test'
# def sendData():
    #filename=input("Ingresa el nombre del archivo que quieres subir")
    #cloudname=input("ingresa el nombre del archivo que quieres en la base de datos")
    #storage.child(cloudname).put(filename)
    # data={'name':"Santiago", 'url':"www.test.com", 'type':"csv"}
    # db.child("files").child("myownid").set(data)    



# @app.route('/', methods=['GET', 'POST'])
# def basic():
# 	if request.method == 'POST':
# 		if request.form['submit'] == 'add':

# 			name = request.form['name']
# 			db.child("todo").push(name)
# 			todo = db.child("todo").get()
# 			to = todo.val()
# 			return render_template('index.html', t=to.values())
# 		elif request.form['submit'] == 'delete':
# 			db.child("todo").remove()
# 		return render_template('index.html')
# 	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)



#auth=firebase.auth()
# storage=firebase.storage()

#Login
#Authentication
#email = input("Enter your email: ")
#password= input("Enter your password: ")
#try: 
#    auth.sign_in_with_email_and_password(email,password)
#    print("Autenticado con exito")
#except:
#    print("Clave incorrecta, intente de nuevo")


#Registro 
#email = input("Ingresa tu  email: ")
#password= input("Ingresa tu contraseña clave: ")
#confirmpass = input("Confirma tu clave")
#if password==confirmpass:
 #   try:    
  #      auth.create_user_with_email_and_password(email,password)       
   #     print("En hora buena")
    #except:
     #   print("Ya existe el email")

#storage
#filename=input("Ingresa el nombre del archivo que quieres subir")
#cloudname=input("ingresa el nombre del archivo que quieres en la base de datos")
#storage.child(cloudname).put(filename)

#print(sorage.child(cloudname).get_url(None))
#url=storage.child(cloudname).get_url(None)
#f=urllib.request.urlopen(url).read()
#print(f)

#download
#cloudname=input("ingresa el nombre del archivo que quieres descargar")
#storage.child("google.txt").download("","downloaded.txt")

# data={'name':"Santiago", 'url':"www.test.com", 'type':"csv"}
# db.child("files").child("myownid").set(data)
