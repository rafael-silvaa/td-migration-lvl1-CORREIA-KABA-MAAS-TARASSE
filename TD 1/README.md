# td-migration-lvl1-CORREIA-KABA-MAAS-TARASSE

Lien du rapport de migration: 

**Journal de Bord - Migration de données**

Initialisation de l'environnement:
  - Installation de MySQL, PostgreSQL et DBeaver
  - Création du dépôt GIT

Création de la base de données
Développement du script Python avec Faker

Migration DBeaver:
  - Configuration des connexions MySQL et PostgreSQL dans l'interface
  - Utilisation de l'outil "Migrate Database" pour copier les tables

Migration Docker et Flyway:
  - Mise en place du fichier docker-compose.yml pour lancer les services
  - Création de l'arborescence Flyway
  - Rédaction des scripts SQL de migration et de test

TEST:
  - Test d'intégrité (s'assurer qu'aucun nom ou email n'est NULL après migration)
  - Vérification du nombre total d'enregistrements 

**MySQL Source**


**PostgreSQL Cible**
  #preuve de migration réussie
  ![image](https://github.com/user-attachments/assets/71d9cb06-573b-44d5-b066-62531505cf89)
  
**Flyway Log**
  #capture d'écran de la console pour voir le succès du "migrate" 


# Repositoire commun pour les 3 TDs

## Niveau 2 : Migration MySQL → PostgreSQL avec Docker et Flyway

### DÉMARRER

```powershell
cd "TD 1"
docker compose down -v
docker compose up -d
Start-Sleep -Seconds 15
```

### VÉRIFIER (migration automatique avec Flyway)

```powershell
docker exec -i mysql-reservation mysql -u app -papp ReservationVoyage -e "SELECT * FROM utilisateurs;"
docker exec -i postgres-reservation psql -U postgres -d reservation_voyage -c "SELECT * FROM utilisateurs;"
```

**Les deux affichent 4 utilisateurs identiques :**
```
id | nom     | prenom | email                      | mot_de_passe
1  | Dupont  | Alice  | alice.dupont@example.com   | motdepasse123
2  | Martin  | Bob    | bob.martin@example.com     | securepass456
3  | Bernard | Claire | claire.bernard@example.com | mypassword789
4  | Petit   | David  | david.petit@example.com    | pass1234
```

### COMMENT ?

1. **MySQL** exécute `001_init.sql` → table + 4 utilisateurs
2. **Flyway** V1 → crée table PostgreSQL
3. **Flyway** V2 → insère les 4 utilisateurs dans PostgreSQL

**Migration réussie quand les deux BDD sont identiques** 