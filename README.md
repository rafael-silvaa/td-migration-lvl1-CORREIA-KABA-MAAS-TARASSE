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
  
**Flyway Log**
  #capture d'écran de la console pour voir le succès du "migrate" 
