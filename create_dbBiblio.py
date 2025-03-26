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


cur.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN) VALUES ('Fondation', 1, 1, 1951, '978-0-123456-47-2')")
cur.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN) VALUES ('Les Misérables', 2, 2, 1862, '978-2-123456-78-3')")
cur.execute("INSERT INTO Livres (titre, id_auteur, id_genre, annee_publication, ISBN) VALUES ('Dune', 2, 2, 1965, '978-2-363456-78-3')")

cur.execute("INSERT INTO Stock (id_livre, quantite) VALUES (1, 3)")
cur.execute("INSERT INTO Stock (id_livre, quantite) VALUES (2, 2)")

cur.execute("INSERT INTO Emprunts (id_utilisateur, id_livre, date_retour_prevu, statut) VALUES (2, 1, '2024-04-01', 'emprunté')")
cursor.execute("SELECT * FROM Livres WHERE statut = 'disponible'")
connection.commit()
connection.close()
    
