USE ReservationVoyage

SET FOREIGN_KEY_CHECKS = 0

DROP TABLE IF EXISTS reservationvoyage.reservations
DROP TABLE IF EXISTS reservationvoyage.utilisateurs

CREATE TABLE Utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(100) NOT NULL,
    Prenom VARCHAR(100) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    MotDePasse VARCHAR(255) NOT NULL
)

CREATE TABLE Reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    IdUtilisateur INT NOT NULL,
    DateReservation DATE NOT NULL,
    Destination VARCHAR(100) NOT NULL,
    Prix DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_user 
        FOREIGN KEY (IdUtilisateur) 
        REFERENCES Utilisateurs(id) 
        ON DELETE CASCADE
)

SET FOREIGN_KEY_CHECKS = 1