import sqlite3 

connection = sqlite3.connect('bibliotheque.db')

with open('schemaBiblio.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

 
cur.execute("INSERT INTO Utilisateurs (nom, prenom, mot_de_passe, role) VALUES ('Admin', 'Super', 'admin', 'admin')")
cur.execute("INSERT INTO Utilisateurs (nom, prenom, mot_de_passe, role) VALUES ('Bulgarean', 'Lavinia', 'password', 'utilisateur')")

cur.execute("INSERT INTO Genres (nom) VALUES ('Science-Fiction')")
cur.execute("INSERT INTO Genres (nom) VALUES ('Roman')")
    
cur.execute("INSERT INTO Auteurs (nom, prenom) VALUES ('Asimov', 'Isaac')")
cur.execute("INSERT INTO Auteurs (nom, prenom) VALUES ('Hugo', 'Victor')")
cur.execute("INSERT INTO Auteurs (nom, prenom) VALUES ('Herbert', 'Frank')")

# Ajout de la colonne "disponible" si elle n'existe pas
cur.execute("PRAGMA table_info(Livres);")
columns = [column[1] for column in cur.fetchall()]
if "disponible" not in columns:
    cur.execute("ALTER TABLE Livres ADD COLUMN disponible INTEGER DEFAULT 1;")

# Ajout de livres avec "disponible = 1" (par défaut)
cur.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN, disponible) VALUES ('Fondation', 1, 1, 1951, '978-0-123456-47-2', 1)")
cur.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN, disponible) VALUES ('Les Misérables', 2, 2, 1862, '978-2-123456-78-3', 1)")
cur.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN, disponible) VALUES ('Dune', 2, 2, 1965, '978-2-363456-78-3', 1)")

# Ajout de stock pour les livres
cur.execute("INSERT INTO Stock (id_livre, quantite) VALUES (1, 3)")
cur.execute("INSERT INTO Stock (id_livre, quantite) VALUES (2, 2)")

# Ajout d'un emprunt (livre pris par l'utilisateur 2, donc il devient indisponible)
cur.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_retour_prevu, statut) VALUES (2, 1, '2024-04-01', 'emprunté')")
cur.execute("UPDATE Livres SET disponible = 0 WHERE id = 1")  # Livre emprunté

# Vérification des livres disponibles
cur.execute("SELECT * FROM Livres WHERE disponible = 1")
livres_disponibles = cur.fetchall()
print("Livres disponibles :", livres_disponibles)

# Validation des changements et fermeture de la connexion
connection.commit()
connection.close()
