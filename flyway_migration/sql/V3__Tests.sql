-- Tests post-migration
DO $$ 
DECLARE
    user_count INT;
BEGIN 
    -- Vérification 1: Pas d'email NULL
    IF (SELECT COUNT(*) FROM utilisateurs WHERE email IS NULL) > 0 THEN 
        RAISE EXCEPTION 'Échec Test: Email NULL trouvé'; 
    END IF;

    -- Vérification 2: Volumétrie (on attend 500 users)
    SELECT COUNT(*) INTO user_count FROM utilisateurs;
    IF user_count < 500 THEN
        RAISE EXCEPTION 'Échec Test: Moins de 500 utilisateurs trouvés (% trouvés)', user_count;
    END IF;
    
    RAISE NOTICE 'Tous les tests sont passés avec succès.';
END $$;