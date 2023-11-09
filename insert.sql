-- Insertion dans la table Style_musique
INSERT INTO Style_musique (id_style_musique, nom_style_musique) VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Hip-Hop'),
(4, 'Jazz');

-- Insertion dans la table Equipement
INSERT INTO Equipement (id_equipement, nom_equipement) VALUES
(1, 'Microphone'),
(2, 'Enceinte'),
(3, 'Batterie'),
(4, 'Guitare électrique');

-- Insertion dans la table Logement
INSERT INTO Logement (id_logement, adresse_ville_codepostal, nom_etablissement, nb_etoile, photo) VALUES
(1, 'Paris 75001', 'Hôtel Parisien', 3, NULL),
(2, 'Marseille 13001', 'Auberge Provençale', 2, NULL),
(3, 'Lyon 69001', 'Grand Hôtel Lyonnais', 4, NULL);

-- Insertion dans la table Artiste
INSERT INTO Artiste (id_artiste, telephone, mail, nom_artiste, prenom_artiste, date_de_naissance, lieu_naissance, adresse, securite_sociale, conge_spectacle, cni, date_delivrance_cni, date_expiration_cni, carte_reduction, id_style_musique, photo, nom_scene) VALUES
(1, '555-123-4567', 'artiste1@example.com', 'John', 'Doe', '1990-05-15', 'New York', '123 Main St', '123-45-6789', 'Oui', 'ABC123456', '2020-01-15', '2025-01-15', 'Réduction1', 1, NULL,'LeoN'),
(2, '555-987-6543', 'artiste2@example.com', 'Jane', 'Smith', '1985-08-20', 'Los Angeles', '456 Elm St', '987-65-4321', 'Non', 'XYZ987654', '2019-06-10', '2024-06-10', 'Réduction2', 2, NULL, 'MyG');

-- Insertion dans la table Jouer
INSERT INTO Jouer (id_artiste, id_style_musique) VALUES
(1, 1),
(1, 2),
(2, 3);

-- Insertion dans la table Type_Salle
INSERT INTO Type_Salle (id_type, type_place_s) VALUES
(1, 'Salle de concert'),
(2, 'Théâtre'),
(3, 'Salle polyvalente'),
(4, 'Scéne de musique');

-- Insertion dans la table Salle
INSERT INTO Salle (id_salle, id_type_salle, loge, nom_salle, nb_places, profondeur_scene, longueur_scene, description_salle, adresse_salle, telephone_salle, photo, accueil_pmr) VALUES
(1, 1, 'Oui', 'Marché Gare', 414, NULL, NULL, 'Le Marché Gare à Lyon est une salle de concert et un lieu culturel de taille plus modeste et intime.', '4 Place Hubert Mounier Lyon', '04 72 40 97 13', NULL, 'Oui'),
(2, 3, 'Non', 'Halle Tony Garnier', 20000, NULL, NULL, "La Halle Tony Garnier à Lyon est l'une des plus grandes salles de spectacles polyvalentes en France.", '20 Place Dr Charles et Christophe Mérieu 69007 Lyon', '04 72 76 85 85', NULL, 'Oui'),
(3, 3, 'Non', 'Toï ToÏ le Zinc', 200, NULL, NULL, "Toï Toï le Zinc à Villeurbanne est un espace culturel polyvalent qui peut accueillir une variété d'événements artistiques et culturels", '17-19 rue Marcel Dutartre 69100 Villeurbanne', '09 51 90 85 04', NULL, NULL),
(4, 3, 'Oui', "L'amphithéatre (Salle 3000)", 4500, NULL, NULL, "L'Amphithéâtre (Salle 3000) à Lyon est une salle de concert et un espace événementiel de grande envergure.", '80 Quai Charles de Gaulle, 69006 Lyon', '04 72 82 26 26', NULL, NULL),
(5, 4, 'Oui', 'Epicerie Moderne', 750, NULL, NULL, 'Gérée par une association, cette salle modulable accueille des concerts variés et propose des expositions.', 'place René Lescot 69320 Feyzin', '04 72 89 98 70', NULL, NULL);


-- Insertion dans la table Concert
INSERT INTO Concert (id_concert, nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert, photo) VALUES
(1, 'Concert Rock', '2023-11-15 20:00:00', 120, 1, 1, "Un festival de sons électrisants vous attend. Joignez-vous à nous pour une nuit de musique inoubliable !", NULL),
(2, 'Concert Pop', '2023-12-10 19:30:00', 90, 2, 2, "Plongez dans un océan de mélodies envoûtantes lors de notre concert exceptionnel. Réservez vos billets dès maintenant !", NULL),
(3, 'Concert Rap', '2022-12-10 19:30:00', 100, 2, 2, "Soyez prêt à vibrer au rythme des hits avec une line-up exceptionnelle. Un concert incontournable pour les amoureux de la musique !", NULL);

-- Insertion dans la table Avoir
INSERT INTO Avoir (id_salle, id_concert, plan_feu, installation, FOH, backline, retour) VALUES
(1, 1, 'Plan Feu A', 'Installation A', 'FOH A', 'Backline A', 'Retour A'),
(2, 2, 'Plan Feu B', 'Installation B', 'FOH B', 'Backline B', 'Retour B');

-- Insertion dans la table Posseder
INSERT INTO Posseder (id_salle, id_equipement, quantite) VALUES
(1, 1, 10),
(1, 2, 8),
(2, 3, 1),
(2, 4, 5);

-- Insertion dans la table Besoin_equipement_artiste
INSERT INTO Besoin_equipement_artiste (id_concert, id_artiste, id_equipement, quantite, quantite_posseder) VALUES
(1, 1, 1, 5, 2),
(1, 1, 2, 4, 4),
(2, 2, 3, 1, 0),
(2, 2, 4, 2, 3);

-- Insertion dans la table Loger
INSERT INTO Loger (id_artiste, id_logement, id_concert, nb_personne, nb_nuit) VALUES
(1, 1, 1, 2, 3),
(2, 2, 2, 1, 2);

-- Insertion dans la table Participer
INSERT INTO Participer (id_concert, id_artiste, transport, restauration) VALUES
(1, 1, 'Voiture', 'Oui'),
(2, 2, 'Avion', 'Non');
