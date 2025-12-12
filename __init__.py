from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

# Initialisation de l'application Flask
app = Flask(__name__)

# Route /contact/ (modifiée pour l'Exercice 5)
@app.route("/contact/")
def MaPremiereAPI():
    # Renvoyer le template du formulaire de contact (contact.html doit exister)
    return render_template("contact.html") 

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

# Route /histogramme/ (Affiche le graphique à colonnes)
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

# =========================================================
# EXERCICE 6 : API et Route pour le Comptage des Commits
# =========================================================

# 1. API qui interroge GitHub et compte les commits par minute
@app.route('/api/v1/commits/')
def get_commits_data():
    # URL de l'API GitHub pour les commits du dépôt (Indice N°1)
    # ATTENTION : Si le repository change, changez l'URL ici
    api_url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    try:
        response = urlopen(api_url)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
    except Exception as e:
        # En cas d'échec de l'appel API (limite de taux atteinte, URL invalide, etc.)
        return jsonify(error=f"Erreur d'appel API GitHub: {e}"), 500
    
    commits_par_minute = {}
    
    for commit in json_content:
        # Extraction de la date (Indice N°2 : [commit][author][date])
        date_string = commit.get('commit', {}).get('author', {}).get('date')
        
        if date_string:
            # Conversion de la chaîne de date en objet datetime (Indice N°3)
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute
            
            # Comptage de la fréquence
            commits_par_minute[minute] = commits_par_minute.get(minute, 0) + 1

    # Préparation du résultat final au format [{Minute: M, Total: N}]
    results = []
    # Assure que toutes les minutes de 0 à 59 sont présentes (important pour le graphique)
    for minute in range(60):
        results.append({
            'minute': minute,
            'total_commits': commits_par_minute.get(minute, 0) 
        })
        
    return jsonify(results=results)


# 2. Route Flask qui affiche le graphique des commits
@app.route("/commits/")
def commits():
    # Flask va chercher "commits.html" dans le dossier 'templates'
    return render_template("commits.html")
# =========================================================

# Route / (Page d'accueil)
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Bloc d'exécution principal
if __name__ == "__main__":
  app.run(debug=True)
