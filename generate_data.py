from faker import Faker
import mysql.connector  
import random
import os

# Configuration
fake = Faker()
OUTPUT_FILE = "/app/flyway_migration/sql/V2__Insert_data.sql"

# Attente de la connexion MySQL (assure-toi que Docker tourne)
try:
    conn = mysql.connector.connect(
        host='mysql',       
        user='root',
        password='root',    
        database='ReservationVoyage'
    )
    cursor = conn.cursor()
    
    # Création table MySQL pour le test (Niveau 1)
    cursor.execute("DROP TABLE IF EXISTS Reservations")
    cursor.execute("DROP TABLE IF EXISTS Utilisateurs")
    cursor.execute("""
        CREATE TABLE Utilisateurs (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            Nom VARCHAR(100), Prenom VARCHAR(100),
            Email VARCHAR(255), MotDePasse VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE Reservations (
            Id INT AUTO_INCREMENT PRIMARY KEY,
            UtilisateurId INT, Destination VARCHAR(100),
            DateReservation DATETIME, Prix DECIMAL(10, 2),
            FOREIGN KEY (UtilisateurId) REFERENCES Utilisateurs(Id)
        )
    """)

    print("Génération des données et écriture du script Flyway...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- Migration des données générées depuis MySQL\n")
        
        user_ids = []
        # 500 Utilisateurs
        for _ in range(500):
            nom = fake.last_name().replace("'", "''") # Échapper les apostrophes
            prenom = fake.first_name().replace("'", "''")
            email = fake.unique.email()
            mdp = fake.password(length=12)
            
            # Insert MySQL
            cursor.execute(f"INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse) VALUES ('{nom}', '{prenom}', '{email}', '{mdp}')")
            user_ids.append(cursor.lastrowid)
            
            # Écriture pour Flyway (PostgreSQL)
            f.write(f"INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse) VALUES ('{nom}', '{prenom}', '{email}', '{mdp}');\n")

        # 1000 Réservations
        for _ in range(1000):
            uid = random.choice(user_ids)
            dest = fake.city().replace("'", "''")
            date = fake.date_time_this_year()
            prix = round(random.uniform(50, 2000), 2)
            
            # Insert MySQL
            cursor.execute(f"INSERT INTO Reservations (UtilisateurId, Destination, DateReservation, Prix) VALUES ({uid}, '{dest}', '{date}', {prix})")
            
            # Écriture pour Flyway (PostgreSQL)
            f.write(f"INSERT INTO Reservations (UtilisateurId, Destination, DateReservation, Prix) VALUES ({uid}, '{dest}', '{date}', {prix});\n")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Succès ! Données insérées dans MySQL et script {OUTPUT_FILE} généré.")

except Exception as e:
    print(f"Erreur : {e}")
    print("Vérifie que ton docker compose tourne (localhost:3306).")