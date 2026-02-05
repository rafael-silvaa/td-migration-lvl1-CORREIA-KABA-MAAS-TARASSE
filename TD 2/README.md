# TD 2 - Migration en ligne avec CDC (GlobeTrotter)

## Objectif (étape 4 uniquement)

Effectuer une migration initiale de MySQL vers PostgreSQL par dump/import, puis vérifier les volumes.

## Démarrage rapide

```powershell
# 1. Lancer tous les conteneurs
docker-compose up -d

# 2. Attendre 15 secondes
Start-Sleep -Seconds 15

# 3. Vérifier que tout tourne
docker-compose ps
```

## Vérifier le système

### Voir les logs en direct
```powershell
docker logs -f gt_app_faker
docker logs -f gt_app_cdc
docker logs gt_app_faker --tail 20
```

### Compter les bookings
```powershell
docker exec gt_mysql mysql -ugt_user -pgt_pass globetrotter -N -e "SELECT COUNT(*) FROM bookings;"
docker exec gt_postgres psql -U gt_user -d globetrotter -t -c "SELECT COUNT(*) FROM bookings;"
```

### Voir les derniers bookings
```powershell
docker exec gt_mysql mysql -ugt_user -pgt_pass globetrotter -N -e "SELECT id, customer_email, destination, status FROM bookings ORDER BY id DESC LIMIT 5;"
```

## 4. Migration bulk (étape 4)

### 4.1 Arrêter faker
```powershell
docker-compose stop app_faker
```

### 4.2 Dump MySQL
```powershell
docker exec gt_mysql mysqldump -ugt_user -pgt_pass --no-tablespaces --no-create-info --skip-triggers --skip-add-locks --skip-disable-keys --compact globetrotter bookings > bookings.sql
```

### 4.3 Adapter dump
```powershell
$content = Get-Content bookings.sql -Raw
$content = $content -replace '`',''
Set-Content bookings_pg.sql $content
```

### 4.4 Créer base dump
```powershell
docker exec gt_postgres psql -U gt_user -d postgres -c "CREATE DATABASE globetrotter_dump;"
docker cp flyway/sql/V1__Create_bookings_table.sql gt_postgres:/tmp/V1__Create_bookings_table.sql
docker exec gt_postgres psql -U gt_user -d globetrotter_dump -f /tmp/V1__Create_bookings_table.sql
```

### 4.5 Importer
```powershell
docker cp bookings_pg.sql gt_postgres:/tmp/bookings_pg.sql
docker exec gt_postgres psql -U gt_user -d globetrotter_dump -f /tmp/bookings_pg.sql
```

### 4.6 Vérifier
```powershell
docker exec gt_mysql mysql -ugt_user -pgt_pass globetrotter -N -e "SELECT COUNT(*) FROM bookings;"
docker exec gt_postgres psql -U gt_user -d globetrotter_dump -t -c "SELECT COUNT(*) FROM bookings;"
```

### 4.7 Redémarrer faker
```powershell
docker-compose start app_faker
```

## Dépannage

```powershell
docker-compose restart gt_app_faker
docker-compose restart gt_app_cdc
docker logs gt_app_cdc --tail 20
```

## Ports
- MySQL: 3307, PostgreSQL: 5433
- User: gt_user / gt_pass
