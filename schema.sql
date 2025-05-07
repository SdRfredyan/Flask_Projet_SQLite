DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS moteur;
DROP TABLE IF EXISTS finition;

CREATE TABLE marque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

CREATE TABLE modele (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    annee TEXT,
    image TEXT,
    marque_id INTEGER,
    FOREIGN KEY (marque_id) REFERENCES marque(id)
);

CREATE TABLE moteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modele_id INTEGER,
    type TEXT CHECK(type IN ('essence', 'diesel')),
    nom TEXT,
    fiabilite TEXT CHECK(fiabilite IN ('fiable', 'moyenne', 'non')),
    FOREIGN KEY (modele_id) REFERENCES modele(id)
);

CREATE TABLE finition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modele_id INTEGER,
    nom TEXT,
    FOREIGN KEY (modele_id) REFERENCES modele(id)
);
