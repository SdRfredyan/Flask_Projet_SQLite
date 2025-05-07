DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS modele;

CREATE TABLE marque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE modele (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    annee TEXT,
    motorisation TEXT,
    consommation TEXT,
    fiabilite TEXT,
    description TEXT,
    marque_id INTEGER NOT NULL,
    FOREIGN KEY (marque_id) REFERENCES marque(id)
);
