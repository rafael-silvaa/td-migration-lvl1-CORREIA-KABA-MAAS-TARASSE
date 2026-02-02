-- Création de la structure pour PostgreSQL
CREATE TABLE Utilisateurs (
    Id SERIAL PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Prenom VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    MotDePasse VARCHAR(255) NOT NULL
);

CREATE TABLE Reservations (
    Id SERIAL PRIMARY KEY,
    UtilisateurId INT,
    Destination VARCHAR(100),
    DateReservation TIMESTAMP,
    Prix DECIMAL(10, 2),
    FOREIGN KEY (UtilisateurId) REFERENCES Utilisateurs(Id)
);