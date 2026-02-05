from faker import Faker
import mysql.connector
import random
from datetime import datetime, timedelta

fake = Faker()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='040116',
    database='ReservationVoyage'
)

cursor = conn.cursor()

nb_users = 500
userids = []  # pour stocker les IDs insérés

for _ in range(nb_users):
    nom = fake.last_name()
    prenom = fake.first_name()
    email = fake.email()
    motdepasse = fake.password(length=12)

    query_user = """
        INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_user, (nom, prenom, email, motdepasse))
    userids.append(cursor.lastrowid)  # récupérer l'ID auto-incrémenté

conn.commit()

nbreservations = 1000

for _ in range(nbreservations):
    # choisir un utilisateur au hasard parmi ceux créés
    id_utilisateur = random.choice(userids)

    # exemple de champs pour la table Reservations
    # adapte les noms de colonnes à ton schéma exact
    date_resa = fake.date_between(start_date='-1y', end_date='today')
    destination = fake.city()
    prix = round(random.uniform(50, 1500), 2)

    query_resa = """
        INSERT INTO Reservations (IdUtilisateur, DateReservation, Destination, Prix)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query_resa, (id_utilisateur, date_resa, destination, prix))

conn.commit()

cursor.close()
conn.close()