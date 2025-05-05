DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS marque;

CREATE TABLE marque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL
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

INSERT INTO marque (nom) VALUES 
('Peugeot'), ('Renault'), ('Toyota');

INSERT INTO modele (nom, annee, motorisation, consommation, fiabilite, description, marque_id) VALUES
('308 II', '2018', '1.2 PureTech', '5.1L/100km', 'Très mauvaise', 'Compacte moderne', 1),
('Clio IV', '2016', '1.5 dCi', '4.3L/100km', 'Très bonne', 'Citadine populaire', 2);
