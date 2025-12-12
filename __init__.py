from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

# Initialisation de l'application Flask
app = Flask(__name__)

# Route /contact/
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

# Route /tawarano/ (API de données filtrées)
@app.route('/tawarano/')
def meteo():
    # Appel de l'API OpenWeatherMap, extraction et conversion K -> °C
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

# Route /rapport/ (Affiche le graphique linéaire)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# =========================================================
# NOUVELLE ROUTE : /histogramme/ (Affiche le graphique à colonnes)
# =========================================================
@app.route("/histogramme/")
def histogramme():
    # Flask va chercher "histogramme.html" dans le dossier 'templates'
    return render_template("histogramme.html")
# =========================================================

# Route / (Page d'accueil)
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Bloc d'exécution principal
if __name__ == "__main__":
  app.run(debug=True)
