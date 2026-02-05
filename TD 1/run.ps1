# --- Script automatique pour Windows (PowerShell) ---
Write-Host "Démarrage..." -ForegroundColor Green

# 1. Vérification et création des tests (Sécurité)
if (-not (Test-Path "tests")) { New-Item -ItemType Directory -Force -Path "tests" | Out-Null }

$v3 = "tests\V3_Test_integrite.sql"
if (-not (Test-Path $v3)) {
    Set-Content -Path $v3 -Value "SELECT COUNT(*) as NULL_NAMES FROM utilisateurs WHERE nom IS NULL;`nSELECT COUNT(*) as NULL_EMAILS FROM utilisateurs WHERE email IS NULL;"
}

$v4 = "tests\V4_Test_completude.sql"
if (-not (Test-Path $v4)) {
    Set-Content -Path $v4 -Value "SELECT COUNT(*) as TOTAL_USERS FROM utilisateurs;"
}

# 2. Lancement de la Migration Flyway
Write-Host "--- 1/2 Migration Flyway ---" -ForegroundColor Cyan
# On utilise ${PWD} pour le chemin actuel et des guillemets pour gérer les espaces
docker run --rm --network host `
  -v "${PWD}/flyway/sql:/flyway/sql" `
  -v "${PWD}/flyway/conf:/flyway/conf" `
  flyway/flyway `
  -configFiles=/flyway/conf/flyway.conf migrate

# 3. Lancement des Tests
Write-Host "--- 2/2 Exécution des tests ---" -ForegroundColor Cyan
$files = Get-ChildItem "tests\*.sql"

foreach ($f in $files) {
    Write-Host "Test : $($f.Name)" -ForegroundColor Yellow
    # Commande compatible Windows pour lire le fichier et l'envoyer à Docker
    Get-Content $f.FullName | docker exec -i postgres-reservation psql -U postgres -d reservation_voyage
}

Write-Host " Terminé !" -ForegroundColor Green