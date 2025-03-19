from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = "votre_clé_secrète"  # Remplacer par une clé secrète plus robuste pour la production

DB_NAME = "bibliotheque.db"

# Fonction de vérification de l'authentification de l'utilisateur
def est_authentifie():
    return session.get('authentifie', False)

def est_admin():
    return session.get('role') == 'admin'

# Connexion à la base de données
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par leur nom
    return conn

# Route d'accueil
@app.route('/bibliotheque')
def index():
    return render_template('index.html')

# Route d'authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Utilisateurs WHERE email = ? AND mot_de_passe = ?", (email, mot_de_passe))
        utilisateur = cursor.fetchone()

        if utilisateur:
            session['authentifie'] = True
            session['user_id'] = utilisateur['id']
            session['role'] = utilisateur['role']
            return redirect(url_for('index'))
        else:
            return render_template('authentification.html', error="Identifiants incorrects")
    
    return render_template('authentification.html')

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.clear()  # Efface la session
    return redirect(url_for('index'))

# Route pour l'enregistrement d'un nouveau livre
@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if not est_admin():
        return redirect(url_for('index'))

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        annee_publication = request.form['annee_publication']
        isbn = request.form['isbn']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN) VALUES (?, ?, ?, ?, ?)",
                       (titre, auteur, genre, annee_publication, isbn))
        conn.commit()
        return redirect(url_for('lister_livres'))

    return render_template('ajouter_livre.html')

# Route pour afficher la liste des livres
@app.route('/lister_livres')
def lister_livres():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Livres")
    livres = cursor.fetchall()
    return render_template('lister_livres.html', livres=livres)

# Route pour supprimer un livre
@app.route('/supprimer_livre/<int:id_livre>', methods=['GET'])
def supprimer_livre(id_livre):
    if not est_admin():
        return redirect(url_for('index'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Livres WHERE id = ?", (id_livre,))
    conn.commit()
    return redirect(url_for('lister_livres'))

# Route pour rechercher des livres disponibles
@app.route('/recherche_livre', methods=['GET', 'POST'])
def recherche_livre():
    if request.method == 'POST':
        search = request.form['search']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Livres WHERE titre LIKE ? OR ISBN LIKE ?", ('%' + search + '%', '%' + search + '%'))
        livres = cursor.fetchall()
        return render_template('recherche_livre.html', livres=livres)
    
    return render_template('recherche_livre.html')

# Route pour emprunter un livre
@app.route('/emprunter_livre/<int:id_livre>', methods=['GET'])
def emprunter_livre(id_livre):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db()
    cursor = conn.cursor()
    
    # Vérification de la disponibilité du livre
    cursor.execute("SELECT * FROM Stock WHERE id_livre = ?", (id_livre,))
    stock = cursor.fetchone()
    if stock and stock['quantite'] > 0:
        date_retour_prevu = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_retour_prevu, statut) VALUES (?, ?, ?, ?)",
                       (session['user_id'], id_livre, date_retour_prevu, 'emprunté'))
        cursor.execute("UPDATE Stock SET quantite = quantite - 1 WHERE id_livre = ?", (id_livre,))
        conn.commit()
        return redirect(url_for('lister_livres'))
    else:
        return "Le livre n'est pas disponible"

# Route pour retourner un livre
@app.route('/retourner_livre/<int:id_emprunt>', methods=['GET'])
def retourner_livre(id_emprunt):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db()
    cursor = conn.cursor()
    
    # Mettre à jour l'emprunt
    cursor.execute("UPDATE Emprunts SET statut = 'retourné', date_retour_effectif = ? WHERE id = ?",
                   (datetime.now().strftime('%Y-%m-%d'), id_emprunt))
    cursor.execute("SELECT id_livre FROM Emprunts WHERE id = ?", (id_emprunt,))
    livre_id = cursor.fetchone()['id_livre']
    
    # Mettre à jour le stock
    cursor.execute("UPDATE Stock SET quantite = quantite + 1 WHERE id_livre = ?", (livre_id,))
    conn.commit()
    return redirect(url_for('index'))

# Route pour gérer les utilisateurs (admin)
@app.route('/gestion_utilisateurs', methods=['GET'])
def gestion_utilisateurs():
    if not est_admin():
        return redirect(url_for('index'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Utilisateurs")
    utilisateurs = cursor.fetchall()
    return render_template('gestion_utilisateurs.html', utilisateurs=utilisateurs)

# Route pour ajouter un utilisateur (admin)
@app.route('/ajouter_utilisateur', methods=['GET', 'POST'])
def ajouter_utilisateur():
    if not est_admin():
        return redirect(url_for('index'))

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']
        role = request.form['role']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (?, ?, ?, ?, ?)",
                       (nom, prenom, email, mot_de_passe, role))
        conn.commit()
        return redirect(url_for('gestion_utilisateurs'))

    return render_template('ajouter_utilisateur.html')

if __name__ == '__main__':
    app.run(debug=True)
