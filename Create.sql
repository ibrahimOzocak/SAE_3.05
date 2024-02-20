CREATE TABLE Style_musique (
  nom_style_musique VARCHAR(42) PRIMARY KEY NOT NULL
);

CREATE TABLE Equipement (
  id_equipement INT PRIMARY KEY NOT NULL,
  nom_equipement VARCHAR(42) UNIQUE
);

CREATE TABLE Logement (
  id_logement INT PRIMARY KEY NOT NULL,
  adresse_ville_codepostal VARCHAR(42),
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
  adresse VARCHAR(42),
  securite_sociale VARCHAR(42),
  conge_spectacle VARCHAR(42),
  cni VARCHAR(42),
  date_delivrance_cni TIMESTAMP,
  date_expiration_cni TIMESTAMP,
  carte_reduction VARCHAR(42),
  nom_style_musique VARCHAR(42),
  nom_scene VARCHAR(42),
  photo LONGBLOB,
  FOREIGN KEY (nom_style_musique) REFERENCES Style_musique (nom_style_musique)
);

CREATE TABLE Jouer (
  id_artiste INT NOT NULL,
  nom_style_musique VARCHAR(42) NOT NULL,
  PRIMARY KEY (id_artiste, nom_style_musique),
  FOREIGN KEY (id_artiste) REFERENCES Artiste (id_artiste),
  FOREIGN KEY (nom_style_musique) REFERENCES Style_musique (nom_style_musique)
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
  id_artiste INT NOT NULL,
  id_equipement INT NOT NULL,
  quantite INT,
  quantite_posseder INT,
  PRIMARY KEY (id_concert, id_artiste, id_equipement),
  FOREIGN KEY (id_equipement) REFERENCES Equipement (id_equipement),
  FOREIGN KEY (id_artiste) REFERENCES Artiste (id_artiste),
  FOREIGN KEY (id_concert) REFERENCES Concert (id_concert)
);

CREATE TABLE Loger (
  id_artiste INT NOT NULL,
  id_logement INT NOT NULL,
  id_concert INT NOT NULL,
  nb_personne INT,
  nb_nuit INT,
  PRIMARY KEY (id_artiste, id_logement, id_concert),
  FOREIGN KEY (id_concert) REFERENCES Concert (id_concert),
  FOREIGN KEY (id_logement) REFERENCES Logement (id_logement),
  FOREIGN KEY (id_artiste) REFERENCES Artiste (id_artiste)
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
    cout_materiels DECIMAL(10, 2),
    cout_artiste DECIMAL(10, 2),
    cout_logement DECIMAL(10, 2),
    cout_autres DECIMAL(10, 2),
    cout_salles DECIMAL(10, 2),
    FOREIGN KEY (id_concert) REFERENCES Concert (id_concert)
);


