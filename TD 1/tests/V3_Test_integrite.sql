
# Création du dossier 'tests' s'il n'existe pas
New-Item -ItemType Directory -Force -Path tests

# Création du fichier V3_Test_integrite.sql
Set-Content -Path tests\V3_Test_integrite.sql -Value "SELECT COUNT(*) AS nb_nom_null FROM utilisateurs WHERE nom IS NULL;
SELECT COUNT(*) AS nb_email_null FROM utilisateurs WHERE email IS NULL;"