INSERT INTO Artiste (id_artiste, telephone, mail, nom_artiste, prenom_artiste, date_de_naissance, lieu_naissance, adresse, securite_social, conge_spectacle, cni, date_delivrance_cni, date_experation_cni, carte_reduction, id_style_musique, plan_feu)
VALUES
('1', '0123456789', 'artiste1@example.com', 'Artiste1', 'Prénom1', '1990-01-01', 'Ville1', 'Adresse1', '1234567890', 'Congé1', 'CNI123', '2022-01-01', '2025-01-01', 'Carte1', '1', 'PlanFeu1'),
('2', '9876543210', 'artiste2@example.com', 'Artiste2', 'Prénom2', '1991-02-02', 'Ville2', 'Adresse2', '0987654321', 'Congé2', 'CNI456', '2022-02-02', '2025-02-02', 'Carte2', '2', 'PlanFeu2'),
('3', '1112223333', 'artiste3@example.com', 'Artiste3', 'Prénom3', '1992-03-03', 'Ville3', 'Adresse3', '1112223333', 'Congé3', 'CNI789', '2022-03-03', '2025-03-03', 'Carte3', '3', 'PlanFeu3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Avoir (id_salle, id_concert, plan_feu, installation, FOH, backline, retour)
VALUES
('1', '1', 'PlanFeu1', 'Installation1', 'FOH1', 'Backline1', 'Retour1'),
('2', '2', 'PlanFeu2', 'Installation2', 'FOH2', 'Backline2', 'Retour2'),
('3', '3', 'PlanFeu3', 'Installation3', 'FOH3', 'Backline3', 'Retour3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Besoin_equipement_artiste (id_concert, id_artiste, id_equipement, quantite, possede_equipement)
VALUES
('1', '1', '1', '5', 'Oui'),
('2', '2', '2', '3', 'Non'),
('3', '3', '3', '7', 'Oui'),
-- Ajoutez 7 autres lignes ici
INSERT INTO Concert (id_concert, nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, photo)
VALUES
('1', 'Concert1', '2023-10-27 20:00:00', '120', '1', '1', 'photo1.jpg'),
('2', 'Concert2', '2023-10-28 19:30:00', '90', '2', '2', 'photo2.jpg'),
('3', 'Concert3', '2023-10-29 21:15:00', '150', '3', '3', 'photo3.jpg');
-- Ajoutez 7 autres lignes ici
INSERT INTO Equipement (id_equipement, nom_equipement)
VALUES
('1', 'Microphone'),
('2', 'Guitare'),
('3', 'Batterie');
-- Ajoutez 7 autres lignes ici
INSERT INTO Equipement_Dispo_Salle (id_salle, id_equipement)
VALUES
('1', '1'),
('2', '2'),
('3', '3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Jouer (id_artiste, id_style_musique)
VALUES
('1', '1'),
('2', '2'),
('3', '3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Logement (id_logement, adresse_ville_codepostal, nom_etablissement, nb_etoile)
VALUES
('1', 'Adresse1', 'Etablissement1', '4'),
('2', 'Adresse2', 'Etablissement2', '3'),
('3', 'Adresse3', 'Etablissement3', '5');
-- Ajoutez 7 autres lignes ici
INSERT INTO Loger (id_artiste, id_logement, id_concert, nb_personne, nb_nuit)
VALUES
('1', '1', '1', '2', '5'),
('2', '2', '2', '3', '4'),
('3', '3', '3', '1', '7');
-- Ajoutez 7 autres lignes ici
INSERT INTO Participer (id_concert, id_artiste, transport, restauration)
VALUES
('1', '1', 'Transport1', 'Restauration1'),
('2', '2', 'Transport2', 'Restauration2'),
('3', '3', 'Transport3', 'Restauration3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Posseder (id_salle, id_equipement)
VALUES
('1', '1'),
('2', '2'),
('3', '3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Salle (id_salle, id_type_salle, loge, nom_salle, nb_places, profondeur_scene, longeur_scene, description_salle, adresse_salle, telephone_salle, id_salle_2)
VALUES
('1', '1', 'Loge1', 'Salle1', '1000', '5', '10', 'Description1', 'AdresseSalle1', '1234567890', '1'),
('2', '2', 'Loge2', 'Salle2', '800', '4', '8', 'Description2', 'AdresseSalle2', '9876543210', '2'),
('3', '3', 'Loge3', 'Salle3', '1200', '6', '12', 'Description3', 'AdresseSalle3', '1112223333', '3');
-- Ajoutez 7 autres lignes ici
INSERT INTO Style_musique (id_style_musique, nom_style_musique)
VALUES
('1', 'Rock'),
('2', 'Pop'),
('3', 'Classique');
-- Ajoutez 7 autres lignes ici
INSERT INTO Type_Salle (id_type, type_place_s, acceuil_pmr, id_salle)
VALUES
('1', 'TypePlace1', 'Oui', '1'),
('2', 'TypePlace2', 'Non', '2'),
('3', 'TypePlace3', 'Oui', '3');
-- Ajoutez 7 autres lignes ici