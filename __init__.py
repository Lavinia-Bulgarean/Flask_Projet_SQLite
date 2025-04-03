from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3 
from datetime import datetime, timedelta
from flask import flash  # Pour afficher des messages
 
app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html') 

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture')) 
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn
# Route d'accueil
@app.route('/bibliotheque')
def accueil():
    return render_template('accueil.html')
# Route pour lister les livres
@app.route('/lister_livres')
def lister_livres():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Récupérer les livres avec leurs auteurs et genres
    cursor.execute("""
        SELECT Livres.titre, Auteurs.nom AS auteur_nom, Auteurs.prenom AS auteur_prenom,
               Genres.nom AS genre, Livres.annee_publication, Livres.ISBN
        FROM Livres
        JOIN Auteurs ON Livres.id_auteur = Auteurs.id
        JOIN Genres ON Livres.id_genre = Genres.id
    """)
    
    livres = cursor.fetchall()  # Récupérer toutes les lignes
    connection.close()

    # Passer les livres récupérés au template
    return render_template('lister_livres.html', livres=livres)

# Route pour ajouter un livre
@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        # Récupération des données du formulaire
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre = request.form['genre']
        annee = request.form['annee']
        isbn = request.form['isbn']

        # Connexion à la base de données
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Vérifier si l'auteur existe déjà dans la base de données
            cursor.execute("SELECT id FROM Auteurs WHERE nom = ? AND prenom = ?", (auteur.split()[0], auteur.split()[1]))
            auteur_id = cursor.fetchone()
            
            if not auteur_id:
                # Si l'auteur n'existe pas, on l'ajoute
                cursor.execute("INSERT INTO Auteurs (nom, prenom) VALUES (?, ?)", (auteur.split()[0], auteur.split()[1]))
                connection.commit()
                
                # Récupérer l'ID du nouvel auteur
                cursor.execute("SELECT id FROM Auteurs WHERE nom = ? AND prenom = ?", (auteur.split()[0], auteur.split()[1]))
                auteur_id = cursor.fetchone()

            # Vérifier si le genre existe dans la base de données
            cursor.execute("SELECT id FROM Genres WHERE nom = ?", (genre,))
            genre_id = cursor.fetchone()
            if not genre_id:
                return "Erreur : Genre introuvable, vérifiez le nom du genre."

            # Insérer le livre dans la base de données
            cursor.execute("""
                INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN)
                VALUES (?, ?, ?, ?, ?)
            """, (titre, auteur_id[0], genre_id[0], annee, isbn))

            # Commit et fermer la connexion
            connection.commit()

        except Exception as e:
            # Gestion des erreurs
            connection.rollback()  # Annuler la transaction en cas d'erreur
            connection.close()
            return f"Erreur lors de l'ajout du livre : {e}"

        # Fermer la connexion à la base de données
        connection.close()

        # Rediriger l'utilisateur vers la page des livres après l'ajout
        return redirect(url_for('lister_livres'))

    return render_template('ajouter_livre.html')
 
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    message = None
    success = False

    if request.method == 'POST':
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Utilisateurs WHERE nom = ? AND mot_de_passe = ?", (nom, mot_de_passe))
        utilisateur = cursor.fetchone()
        connection.close()

        if utilisateur:
            session['utilisateur_id'] = utilisateur['id']
            session['nom'] = utilisateur['nom']
            success = True
            message = "Authentification réussie ! Redirection..."

            # Vérifie si l'utilisateur voulait emprunter un livre avant la connexion
            if 'id_livre' in session:
                id_livre = session.pop('id_livre')  # Récupère et supprime la variable temporaire
                return redirect(url_for('emprunter_livre', id_livre=id_livre))

        else:
            message = "Échec de connexion : Vérifiez votre nom et mot de passe."

    return render_template('connexion.html', message=message, success=success)

# Vérifier si l'utilisateur est connecté
@app.route('/deconnexion')
def deconnexion():
    session.clear()  # Supprimer les données de session
    return redirect(url_for('accueil'))  # Rediriger vers l'accueil


@app.route('/livres_disponibles')
def livres_disponibles():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Livres.id, Livres.titre, Auteurs.nom, Auteurs.prenom, Genres.nom AS genre
        FROM Livres
        JOIN Auteurs ON Livres.id_auteur = Auteurs.id
        JOIN Genres ON Livres.id_genre = Genres.id
        WHERE Livres.id NOT IN (
            SELECT id_livre FROM Emprunts WHERE statut = 'emprunté'
        )
    """)
    
    livres = cursor.fetchall()
    connection.close()
    
    return render_template('livres_disponibles.html', livres=livres)

@app.route('/emprunter/<int:id_livre>', methods=['GET', 'POST'])
def emprunter_livre(id_livre):
    if 'utilisateur_id' not in session:
        # Stocke temporairement l'ID du livre pour redirection après connexion
        session['id_livre'] = id_livre  
        flash("Veuillez vous connecter pour emprunter un livre.", "warning")
        return redirect(url_for('connexion'))  # Redirige vers la connexion

    id_utilisateur = session['utilisateur_id']
    date_retour_prevu = datetime.now() + timedelta(days=14)  # Prêt pour 14 jours

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Vérifier si le livre est déjà emprunté
        cursor.execute("""
            SELECT id FROM Emprunts WHERE id_livre = ? AND statut = 'emprunté'
        """, (id_livre,))
        emprunt_existant = cursor.fetchone()

        if emprunt_existant:
            flash("Ce livre est déjà emprunté.", "danger")
        else:
            # Ajouter l'emprunt à la base de données
            cursor.execute("""
                INSERT INTO Emprunts (id_utilisateur, id_livre, date_retour_prevu, statut)
                VALUES (?, ?, ?, 'emprunté')
            """, (id_utilisateur, id_livre, date_retour_prevu.strftime('%Y-%m-%d')))
            connection.commit()
            flash("Livre emprunté avec succès !", "success")

    except sqlite3.Error as e:
        flash(f"Erreur lors de l'emprunt : {e}", "danger")
    
    connection.close()

    return redirect(url_for('mes_emprunts'))

@app.route('/mes_emprunts')
def mes_emprunts():
    if 'utilisateur_id' not in session:
        flash("Veuillez vous connecter pour voir vos emprunts.", "warning")
        return redirect(url_for('connexion'))

    id_utilisateur = session['utilisateur_id']

    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT Livres.titre, Auteurs.nom, Auteurs.prenom, 
               Emprunts.date_emprunt, Emprunts.date_retour_prevu, Emprunts.statut
        FROM Emprunts
        JOIN Livres ON Emprunts.id_livre = Livres.id
        JOIN Auteurs ON Livres.id_auteur = Auteurs.id
        WHERE Emprunts.id_utilisateur = ? 
        ORDER BY Emprunts.date_emprunt DESC
    """, (id_utilisateur,))
    
    emprunts = cursor.fetchall()
    connection.close()
    
    return render_template('mes_emprunts.html', emprunts=emprunts)

@app.route('/retourner/<int:id_livre>')
def retourner_livre(id_livre):
    if 'utilisateur_id' not in session:
        return redirect(url_for('connexion'))

    id_utilisateur = session['utilisateur_id']

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE Emprunts
        SET statut = 'retourné', date_retour_effectif = CURRENT_DATE
        WHERE id_utilisateur = ? AND id_livre = ? AND statut = 'emprunté'
    """, (id_utilisateur, id_livre))
    connection.commit()
    connection.close()

    return redirect(url_for('mes_emprunts'))


if __name__ == "__main__":
  app.run(debug=True)
