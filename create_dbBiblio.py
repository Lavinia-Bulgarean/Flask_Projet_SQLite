import sqlite3

# Nom du fichier de la base de données
DB_NAME = "bibliotheque.db"

# Schéma SQL de la base de données
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS Utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'utilisateur')) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Auteurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(255) NOT NULL,
    id_auteur INTEGER NOT NULL,
    id_genre INTEGER NOT NULL,
    annee_publication INTEGER,
    ISBN VARCHAR(20) UNIQUE NOT NULL,
    FOREIGN KEY (id_auteur) REFERENCES Auteurs(id) ON DELETE CASCADE,
    FOREIGN KEY (id_genre) REFERENCES Genres(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER NOT NULL,
    quantite INTEGER NOT NULL CHECK (quantite >= 0),
    FOREIGN KEY (id_livre) REFERENCES Livres(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    id_livre INTEGER NOT NULL,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour_prevu DATE NOT NULL,
    date_retour_effectif DATE,
    statut VARCHAR(20) CHECK (statut IN ('emprunté', 'retourné', 'en retard')) DEFAULT 'emprunté',
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id) ON DELETE CASCADE
);
"""

# Fonction pour initialiser la base de données
def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Création des tables
    cursor.executescript(SCHEMA_SQL)

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
