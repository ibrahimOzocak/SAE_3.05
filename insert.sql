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
INSERT INTO Logement (id_logement, adresse_ville_codepostal, nom_etablissement, nb_etoile) VALUES
(1, 'Paris 75001', 'Hôtel Parisien', 3),
(2, 'Marseille 13001', 'Auberge Provençale', 2),
(3, 'Lyon 69001', 'Grand Hôtel Lyonnais', 4);

-- Insertion dans la table Artiste
INSERT INTO Artiste (id_artiste, telephone, mail, nom_artiste, prenom_artiste, date_de_naissance, lieu_naissance, adresse, securite_social, conge_spectacle, cni, date_delivrance_cni, date_expiration_cni, carte_reduction, id_style_musique) VALUES
(1, '555-123-4567', 'artiste1@example.com', 'John', 'Doe', '1990-05-15', 'New York', '123 Main St', '123-45-6789', 'Oui', 'ABC123456', '2020-01-15', '2025-01-15', 'Réduction1', 1),
(2, '555-987-6543', 'artiste2@example.com', 'Jane', 'Smith', '1985-08-20', 'Los Angeles', '456 Elm St', '987-65-4321', 'Non', 'XYZ987654', '2019-06-10', '2024-06-10', 'Réduction2', 2);

-- Insertion dans la table Jouer
INSERT INTO Jouer (id_artiste, id_style_musique) VALUES
(1, 1),
(1, 2),
(2, 3);

-- Insertion dans la table Type_Salle
INSERT INTO Type_Salle (id_type, type_place_s, accueil_pmr) VALUES
(1, 'Salle de concert', true),
(2, 'Théâtre', false),
(3, 'Salle polyvalente', true);

-- Insertion dans la table Salle
INSERT INTO Salle (id_salle, id_type_salle, loge, nom_salle, nb_places, profondeur_scene, longueur_scene, description_salle, adresse_salle, telephone_salle) VALUES
(1, 1, 'Oui', 'Salle de Concert A', 500, 10, 20, 'Salle de concert moderne', '123 Main St, Paris', '555-111-2222'),
(2, 2, 'Non', 'Théâtre B', 300, 8, 15, 'Théâtre classique', '456 Elm St, Marseille', '555-333-4444');

-- Insertion dans la table Concert
INSERT INTO Concert (id_concert, nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, photo) VALUES
(1, 'Concert Rock', '2023-11-15 20:00:00', 120, 1, 1, NULL),
(2, 'Concert Pop', '2023-12-10 19:30:00', 90, 2, 2, NULL);

-- Insertion dans la table Avoir
INSERT INTO Avoir (id_salle, id_concert, plan_feu, installation, FOH, backline, retour) VALUES
(1, 1, 'Plan Feu A', 'Installation A', 'FOH A', 'Backline A', 'Retour A'),
(2, 2, 'Plan Feu B', 'Installation B', 'FOH B', 'Backline B', 'Retour B');

-- Insertion dans la table Posseder
INSERT INTO Posseder (id_salle, id_equipement, quantite) VALUES
(1, 1, '10 microphones'),
(1, 2, '8 enceintes'),
(2, 3, '1 batterie'),
(2, 4, '5 guitares électriques');

-- Insertion dans la table Besoin_equipement_artiste
INSERT INTO Besoin_equipement_artiste (id_concert, id_artiste, id_equipement, quantite, possede_equipement) VALUES
(1, 1, 1, '5 microphones', 'Oui'),
(1, 1, 2, '4 enceintes', 'Oui'),
(2, 2, 3, '1 batterie', 'Non'),
(2, 2, 4, '2 guitares électriques', 'Oui');

-- Insertion dans la table Loger
INSERT INTO Loger (id_artiste, id_logement, id_concert, nb_personne, nb_nuit) VALUES
(1, 1, 1, 2, 3),
(2, 2, 2, 1, 2);

-- Insertion dans la table Participer
INSERT INTO Participer (id_concert, id_artiste, transport, restauration) VALUES
(1, 1, 'Voiture', 'Oui'),
(2, 2, 'Avion', 'Non');
