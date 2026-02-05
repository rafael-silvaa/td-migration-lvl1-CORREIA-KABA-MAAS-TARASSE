from faker import Faker
import mysql.connector
import random

fake = Faker()

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '040116',
    'database': 'ReservationVoyage'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # reset total
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("TRUNCATE TABLE Reservations")
    cursor.execute("TRUNCATE TABLE Utilisateurs")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()

    # users
    nb_users = 500
    userids = []
    
    query_user = """
        INSERT INTO Utilisateurs (Nom, Prenom, Email, MotDePasse)
        VALUES (%s, %s, %s, %s)
    """
    
    for _ in range(nb_users):
        params = (fake.last_name(), fake.first_name(), fake.unique.email(), fake.password(length=12))
        cursor.execute(query_user, params)
        userids.append(cursor.lastrowid)

    conn.commit()

    # reservations
    nb_reservations = 1000
    
    query_resa = """
        INSERT INTO Reservations (IdUtilisateur, DateReservation, Destination, Prix)
        VALUES (%s, %s, %s, %s)
    """

    for _ in range(nb_reservations):
        id_utilisateur = random.choice(userids)
        date_resa = fake.date_between(start_date='-1y', end_date='today')
        destination = fake.city()
        prix = round(random.uniform(50, 1500), 2)
        
        cursor.execute(query_resa, (id_utilisateur, date_resa, destination, prix))

    conn.commit()

except mysql.connector.Error as err:
    print(f"Erreur: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()