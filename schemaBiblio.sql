CREATE TABLE Utilisateurs ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'utilisateur')) NOT NULL
);

CREATE TABLE Genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Auteurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL
);

CREATE TABLE Livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(255) NOT NULL,
    id_auteur INTEGER NOT NULL,
    id_genre INTEGER NOT NULL,
    annee_publication INTEGER,
    ISBN VARCHAR(20) UNIQUE NOT NULL,
    disponible INTEGER DEFAULT 1,  -- ✅ Ajout correct de la colonne "disponible"
    FOREIGN KEY (id_auteur) REFERENCES Auteurs(id) ON DELETE CASCADE,
    FOREIGN KEY (id_genre) REFERENCES Genres(id) ON DELETE SET NULL
);

CREATE TABLE Stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER NOT NULL,
    quantite INTEGER NOT NULL CHECK (quantite >= 0),
    FOREIGN KEY (id_livre) REFERENCES Livres(id) ON DELETE CASCADE
);

CREATE TABLE Emprunts (
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
