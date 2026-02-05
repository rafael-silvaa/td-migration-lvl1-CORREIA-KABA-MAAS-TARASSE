# TD 2 - Migration en ligne avec CDC (GlobeTrotter)

## Objectif (etape 4 uniquement)

Effectuer une migration initiale de MySQL vers PostgreSQL par dump/import, puis verifier les volumes.

## 4. Migration initiale MySQL -> PostgreSQL (bulk)

### 4.1 Dump MySQL

```powershell
docker exec gt_mysql mysqldump -ugt_user -pgt_pass globetrotter bookings > bookings.sql
```

### 4.2 Adapter le dump pour PostgreSQL

Le dump MySQL peut contenir des syntaxes non compatibles (ENGINE=, AUTO_INCREMENT, etc.).
Ouvrir `bookings.sql` et :

- Supprimer `ENGINE=...` et `AUTO_INCREMENT=...`
- Remplacer `INT` par `INTEGER` si besoin
- Supprimer les lignes `LOCK TABLES` / `UNLOCK TABLES`

### 4.3 Importer dans PostgreSQL

```powershell
docker cp bookings.sql gt_postgres:/tmp/bookings.sql
docker exec -it gt_postgres psql -U gt_user -d globetrotter -f /tmp/bookings.sql
```

### 4.4 Verifier les volumes

```powershell
docker exec gt_mysql mysql -ugt_user -pgt_pass globetrotter -e "SELECT COUNT(*) FROM bookings;"
docker exec gt_postgres psql -U gt_user -d globetrotter -c "SELECT COUNT(*) FROM bookings;"
```

## Demarrer / Arreter

```powershell
docker-compose up -d
docker-compose down
```

## Notes rapides

- MySQL port externe : 3307
- PostgreSQL port externe : 5433
- Si erreur d'import, verifier le format SQL MySQL vs PostgreSQL
