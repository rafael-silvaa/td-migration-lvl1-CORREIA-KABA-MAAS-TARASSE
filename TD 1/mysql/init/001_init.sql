CREATE TABLE utilisateurs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  mot_de_passe VARCHAR(255) NOT NULL,
  date_creation TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe)
VALUES 
  ('Dupont', 'Alice', 'alice.dupont@example.com', 'motdepasse123'),
  ('Martin', 'Bob', 'bob.martin@example.com', 'securepass456'),
  ('Bernard', 'Claire', 'claire.bernard@example.com', 'mypassword789'),
  ('Petit', 'David', 'david.petit@example.com', 'pass1234');
