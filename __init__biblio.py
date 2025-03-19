from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Remplacer par une clé secrète plus robuste pour la production

# Fonction de vérification de l'authentification de l'utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/bibliotheque')
def index():
    return render_template('index.html')

# Connexion à la base de données
conn = sqlite3.connect('bibliotheque.db')
cursor = conn.cursor()


if __name__ == '__main__':
    app.run(debug=True)
