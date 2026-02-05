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

