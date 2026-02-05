#!/bin/bash

# --- 1. Exécution des migrations Flyway ---
echo " Lancement de la migration Flyway..."

docker run --rm \
  --network host \
  -v $(pwd)/flyway/sql:/flyway/sql \
  -v $(pwd)/flyway/conf:/flyway/conf \
  flyway/flyway \
  -configFiles=/flyway/conf/flyway.conf migrate
.

# --- 2. Exécution des tests post-migration ---
echo " Lancement des tests de vérification..."

DB_USER="postgres"
DB_NAME="reservation_voyage"
CONTAINER_NAME="postgres-reservation" 

for test_script in tests/*.sql; do
    echo " Exécution de $(basename "$test_script")"
    
    # On exécute la commande psql directement DANS le conteneur postgres
    docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME < "$test_script"
done

echo " Terminé !"