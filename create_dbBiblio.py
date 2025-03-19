import sqlite3

# Nom du fichier de la base de données
DB_NAME = "bibliotheque.db"

# Fonction pour initialiser la base de données
def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Création des tables
    cursor.executescript(schemaBiblio.sql)

    # Ajout de données de test
    cursor.execute("INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES ('Admin', 'Super', 'admin@biblio.com', 'admin123', 'admin')")
    cursor.execute("INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES ('Doe', 'John', 'john.doe@gmail.com', 'password', 'utilisateur')")

    cursor.execute("INSERT INTO Genres (nom) VALUES ('Science-Fiction')")
    cursor.execute("INSERT INTO Genres (nom) VALUES ('Roman')")
    
    cursor.execute("INSERT INTO Auteurs (nom, prenom) VALUES ('Asimov', 'Isaac')")
    cursor.execute("INSERT INTO Auteurs (nom, prenom) VALUES ('Hugo', 'Victor')")

    cursor.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN) VALUES ('Fondation', 1, 1, 1951, '978-0-123456-47-2')")
    cursor.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN) VALUES ('Les Misérables', 2, 2, 1862, '978-2-123456-78-3')")

    cursor.execute("INSERT INTO Stock (id_livre, quantite) VALUES (1, 3)")
    cursor.execute("INSERT INTO Stock (id_livre, quantite) VALUES (2, 2)")

    cursor.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_retour_prevu, statut) VALUES (2, 1, '2024-04-01', 'emprunté')")

    connection.commit()
    connection.close()
    print("✅ Base de données initialisée avec succès !")

# Exécuter la fonction d'initialisation
if __name__ == "__main__":
    init_db()
