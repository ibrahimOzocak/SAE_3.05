CREATE TABLE Style_musique (
  id_style_musique INT PRIMARY KEY NOT NULL,
  nom_style_musique VARCHAR(42) UNIQUE NOT NULL
);

CREATE TABLE Equipement (
  id_equipement INT PRIMARY KEY NOT NULL,
  nom_equipement VARCHAR(42) UNIQUE
);

CREATE TABLE Logement (
  id_logement INT PRIMARY KEY NOT NULL,
  adresse_ville_codepostal VARCHAR(500),
  nom_etablissement VARCHAR(42),
  nb_etoile INT,
  photo LONGBLOB
);

CREATE TABLE Artiste (
  id_artiste INT PRIMARY KEY NOT NULL,
  telephone VARCHAR(42),
  mail VARCHAR(42),
  nom_artiste VARCHAR(42),
  prenom_artiste VARCHAR(42),
  date_de_naissance TIMESTAMP,
  lieu_naissance VARCHAR(42),
  adresse VARCHAR(500),
  securite_sociale VARCHAR(42),
  conge_spectacle VARCHAR(42),
  cni VARCHAR(42),
  date_delivrance_cni TIMESTAMP,
  date_expiration_cni TIMESTAMP,
  carte_reduction VARCHAR(42),
  nom_scene VARCHAR(42),
  photo LONGBLOB
);

CREATE TABLE Jouer (
  id_artiste INT NOT NULL,
  id_style_musique INT NOT NULL,
  PRIMARY KEY (id_artiste, id_style_musique),
  FOREIGN KEY (id_artiste) REFERENCES Artiste (id_artiste),
  FOREIGN KEY (id_style_musique) REFERENCES Style_musique (id_style_musique)
);

CREATE TABLE Type_Salle (
  id_type INT PRIMARY KEY NOT NULL,
  type_place_s VARCHAR(42) UNIQUE
);

CREATE TABLE Salle (
  id_salle INT PRIMARY KEY NOT NULL,
  id_type_salle INT,
  loge VARCHAR(42),
  nom_salle VARCHAR(42),
  nb_places INT,
  profondeur_scene INT,
  longueur_scene INT,
  description_salle VARCHAR(500),
  adresse_salle VARCHAR(500),
  telephone_salle VARCHAR(42),
  photo LONGBLOB,
  accueil_pmr VARCHAR(42),
  FOREIGN KEY (id_type_salle) REFERENCES Type_Salle (id_type)
);

CREATE TABLE Concert (
  id_concert INT PRIMARY KEY NOT NULL,
  nom_concert VARCHAR(42),
  date_heure_concert TIMESTAMP,
  duree_concert INT,
  id_artiste INT NULL,
  id_salle INT NULL,
  description_concert VARCHAR(500),
  photo LONGBLOB,
  FOREIGN KEY (id_artiste) REFERENCES Artiste (id_artiste),
  FOREIGN KEY (id_salle) REFERENCES Salle (id_salle)
);

CREATE TABLE Avoir (
  id_salle INT NOT NULL,
  id_concert INT NOT NULL,
  plan_feu VARCHAR(42),
  installation VARCHAR(42),
  FOH VARCHAR(42),
  backline VARCHAR(42),
  retour VARCHAR(42),
  PRIMARY KEY (id_salle, id_concert),
  FOREIGN KEY (id_concert) REFERENCES Concert (id_concert),
  FOREIGN KEY (id_salle) REFERENCES Salle (id_salle)
);

CREATE TABLE Posseder (
  id_salle INT NOT NULL,
  id_equipement INT NOT NULL,
  quantite INT,
  PRIMARY KEY (id_salle, id_equipement),
  FOREIGN KEY (id_equipement) REFERENCES Equipement (id_equipement),
  FOREIGN KEY (id_salle) REFERENCES Salle (id_salle)
);

CREATE TABLE Besoin_equipement_artiste (
  id_concert INT NOT NULL,
  id_equipement INT NOT NULL,
  quantite INT,
  quantite_posseder INT,
  PRIMARY KEY (id_concert, id_equipement),
  FOREIGN KEY (id_equipement) REFERENCES Equipement (id_equipement),
  FOREIGN KEY (id_concert) REFERENCES Concert (id_concert)
);

CREATE TABLE Loger (
  id_logement INT NOT NULL,
  id_concert INT NOT NULL,
  nb_nuit INT,
  PRIMARY KEY (id_logement, id_concert),
  FOREIGN KEY (id_concert) REFERENCES Concert (id_concert),
  FOREIGN KEY (id_logement) REFERENCES Logement (id_logement)
);

CREATE TABLE Participer (
  id_concert INT NOT NULL,
  id_artiste INT NOT NULL,
  transport VARCHAR(42),
  restauration VARCHAR(42),
  PRIMARY KEY (id_concert, id_artiste),
  FOREIGN KEY (id_artiste) REFERENCES Artiste (id_artiste),
  FOREIGN KEY (id_concert) REFERENCES Concert (id_concert)
);

CREATE TABLE DetailsCouts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_concert INT,
    cout_materiels DECIMAL(10, 2) NULL,
    cout_artiste DECIMAL(10, 2) NULL,
    cout_logement DECIMAL(10, 2) NULL,
    cout_autres DECIMAL(10, 2) NULL,
    cout_salles DECIMAL(10, 2) NULL,
    FOREIGN KEY (id_concert) REFERENCES Concert (id_concert)
);


