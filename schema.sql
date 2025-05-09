DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS motorisation;
DROP TABLE IF EXISTS finition;

CREATE TABLE marque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE
);

CREATE TABLE modele (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    annee_debut INTEGER,
    annee_fin INTEGER,
    description TEXT,
    marque_id INTEGER NOT NULL,
    FOREIGN KEY (marque_id) REFERENCES marque(id)
);

CREATE TABLE motorisation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modele_id INTEGER NOT NULL,
    type TEXT CHECK(type IN ('essence', 'diesel', 'hybride')) NOT NULL,
    nom TEXT NOT NULL, -- Exemple : '2.0L S16'
    puissance TEXT,    -- Exemple : '100 - 150 cv'
    fiabilite TEXT CHECK(fiabilite IN ('fiable', 'moyenne', 'non-fiable')) NOT NULL,
    FOREIGN KEY (modele_id) REFERENCES modele(id)
);

CREATE TABLE finition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modele_id INTEGER NOT NULL,
    nom TEXT NOT NULL,
    FOREIGN KEY (modele_id) REFERENCES modele(id)
);
