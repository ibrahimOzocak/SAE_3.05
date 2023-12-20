import mysql.connector
from PIL import Image
import io
from io import BytesIO
import datetime

HEURES1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
JOUR_VOULU = datetime.datetime.now()

db = mysql.connector.connect(host="servinfo-maria",
                             user="sevellec",
                             password="sevellec",
                             database="DBsevellec")


def get_cursor():
    return db.cursor()


def close_cursor(cursor):
    cursor.close()


def execute_query(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)


def prochains_concerts():
    try:
        cursor = get_cursor()
        req1 = "SELECT * FROM Concert WHERE date_heure_concert >= NOW() ORDER BY date_heure_concert ASC;"
        execute_query(cursor, req1)
        infos = cursor.fetchall()
        close_cursor(cursor)
        for i in infos:
            if i[-1] is not None:
                try:
                    get_image(int(i[0]), "concerts", i[-1])
                except Exception as e:
                    print(e.args)
        return infos
    except Exception as e:
        print(e.args)
        return []


def save_concert(id, nom_concert, date_heure_concert, duree_concert,
                 id_artiste, id_salle, description_concert, photo):
    try:
        cursor = get_cursor()
        req = "INSERT INTO Concert (id_concert,nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert, photo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            req,
            (id, nom_concert, date_heure_concert, duree_concert, id_artiste,
             id_salle, description_concert, save_image(photo)))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def save_salle(id, nom_salle, nb_places, profondeur_scene, longueur_scene,
               telephone_salle, type_place, description_salle, photo,
               adresse_salle, loge, acces_pmr):
    try:
        cursor = get_cursor()
        req = "INSERT INTO Salle (id_salle, id_type_salle, loge, nom_salle, nb_places, profondeur_scene, longueur_scene, description_salle,adresse_salle,telephone_salle, accueil_pmr, photo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            req,
            (id, get_id_type_salles(type_place), loge, nom_salle, nb_places,
             profondeur_scene, longueur_scene, description_salle,
             adresse_salle, telephone_salle, acces_pmr, save_image(photo)))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def save_logement(id, nom_etablissement, adresse_ville_codepostal, nb_etoile):
    try:
        cursor = get_cursor()
        req = "INSERT INTO Logement (id_logement, nom_etablissement, adresse_ville_codepostal, nb_etoile, photo) VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(
            req,
            (id, nom_etablissement, adresse_ville_codepostal, nb_etoile, None))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def save_image(photo):
    try:
        if photo.filename != "":
            photo.seek(0)
            image_data = photo.read()
            image_bytesio = io.BytesIO(image_data)
            blob = image_bytesio.read()
            return blob
    except Exception as e:
        print(e.args)
    return None


def get_image(id_value, repository_name, image_data):
    if id_value is None or image_data is None:
        print("No valid input data")
        return
    try:
        if not isinstance(image_data, bytes):
            image_data.seek(0)
            image_data = image_data.read()
        if len(image_data) > 0:
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')
            nom_fichier = f"ConcertPro/static/images/{repository_name}/{str(id_value)}.jpg"
            image.save(nom_fichier)
    except Exception as e:
        print(f"Error processing image: {str(e)}")


# fonctions utiles pour les templates
def get_concert(id):
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where id_concert= %s"
        cursor.execute(requete, (id, ))
        info = cursor.fetchall()
        if info[0][-1] is not None:
            try:
                get_image(int(info[0][0]), "concerts", info[0][-1])
            except Exception:
                pass
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None


def get_salle(id):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Salle WHERE id_salle = %s"
        cursor.execute(request, (id, ))
        info = cursor.fetchall()
        if info[0][-2] is not None:
            get_image(int(info[0][0]), "salle", info[0][-2])
        close_cursor(cursor)
        return info[0] if info else None
    except Exception as e:
        print(e.args)
        return None


def get_logement(id_logement):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Logement where id_logement = %s"
        cursor.execute(request, (id_logement, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None


def get_artiste(id):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Artiste where id_artiste= %s"
        cursor.execute(request, (id, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_id_type_salle(nom):
    try:
        cursor = get_cursor()
        request = "SELECT id_type FROM Type_Salle where type_place_s= %s"
        cursor.execute(request, (nom, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        if info == []:
            # à la place rajouter le type dans la base de données
            return 1
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def styles_musisque():
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Style_musique"
        cursor.execute(request)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None

def get_styles_musique_artiste(id_artiste):
    try:
        cursor = get_cursor()
        request = "SELECT nom_style_musique FROM Artiste WHERE id_artiste = %s"
        cursor.execute(request, (id_artiste,))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def historique_concerts():
    historique_concerts = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where date_heure_concert < NOW()"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            historique_concerts.append(i)
            if i[-1] is not None:
                try:
                    get_image(int(i[0]), "concerts", i[-1])
                except Exception as e:
                    print(e.args)
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return historique_concerts


def concerts():
    concerts = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            concerts.append(i)
            if i[-1] is not None:
                try:
                    get_image(int(i[0]), "concerts", i[-1])
                except Exception as e:
                    print(e.args)
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return concerts


def salles():
    salles = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Salle"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            salles.append(i)
            if i[-2] is not None:
                get_image(int(i[0]), "salle", i[-2])
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return salles


def artistes():
    artistes = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Artiste"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            if i[-1] is not None and len(i[-1]) != 0:
                get_image(int(i[0]), "artiste", i[-1])
            else:
                i2 = []
                for ind in range(len(i)):
                    if ind == len(i) - 1:
                        i2.append(None)
                    else:
                        i2.append(i[ind])
                i = i2
            artistes.append(i)
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return artistes


def logements():
    logements = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Logement"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            logements.append(i)
            if i[-1] is not None:
                get_image(i[0], "logement", i[-1])  # Probleme avec les images
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return logements


def get_id_concert_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_concert) FROM Concert"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        val = info[0][0]
        if val is not None:
            return info[0][0]
    except Exception as e:
        print(e.args)
    return 0

def get_id_artiste_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_artiste) FROM Artiste"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        val = info[0][0]
        if val is not None:
            return info[0][0]
    except Exception as e:
        print(e.args)
    return 0

def get_id_salle_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_salle) FROM Salle"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        val = info[0][0]
        if val is not None:
            return info[0][0]
    except Exception as e:
        print(e.args)
    return 0

def get_id_logement_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_logement) FROM Logement"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        val = info[0][0]
        if val is not None:
            return info[0][0]
    except Exception as e:
        print(e.args)
    return 0

def get_id_equipement_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_equipement) FROM Equipement"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        val = info[0][0]
        if val is not None:
            return info[0][0]
    except Exception as e:
        print(e.args)
    return 0

def get_id_type_salle_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_type) FROM Type_Salle"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        val = info[0][0]
        if val is not None:
            return info[0][0]
    except Exception as e:
        print(e.args)
    return 0
    return 0


def confirmer_modif_concert(id_concert, nom_concert, date_heure_concert,
                            duree_concert, id_artiste, id_salle,
                            description_concert, photo):
    try:
        cursor = get_cursor()
        if (photo.filename != ""):
            get_image(int(id_concert), "concerts", photo)
            requete = f"UPDATE Concert SET nom_concert = %s, date_heure_concert = %s, duree_concert = %s, id_artiste = %s, id_salle = %s, description_concert = %s, photo = %s WHERE id_concert = %s"
            execute_query(
                cursor, requete,
                (nom_concert, date_heure_concert, duree_concert, id_artiste,
                 id_salle, description_concert, save_image(photo), id_concert))
        else:
            requete = f"UPDATE Concert SET nom_concert = %s, date_heure_concert = %s, duree_concert = %s, id_artiste = %s, id_salle = %s, description_concert = %s WHERE id_concert = %s"
            execute_query(
                cursor, requete,
                (nom_concert, date_heure_concert, duree_concert, id_artiste,
                 id_salle, description_concert, id_concert))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def confirmer_modif_artiste(id_artiste, nom_artiste, prenom_artiste,
                            nom_de_scene, mail, telephone, date_de_naissance,
                            lieu_de_naissance, adresse, numero_secu_sociale,
                            cni, date_delivrance_cni, date_expiration_cni,
                            carte_reduction, genre_musical, photo):
    try:
        get_image(id_artiste, "artiste", photo)
        cursor = get_cursor()
        if photo.filename != "":
            print("none")
            get_image(int(id_artiste), "artiste", photo)
            requete = """
                UPDATE Artiste SET
                telephone = %s, mail = %s,
                nom_artiste = %s, prenom_artiste = %s,
                date_de_naissance = %s, lieu_naissance = %s, adresse = %s,
                securite_sociale = %s, cni = %s, date_delivrance_cni = %s,
                date_expiration_cni = %s, carte_reduction = %s, 
                nom_style_musique = %s, nom_scene = %s, photo = %s
                WHERE id_artiste = %s
            """
            execute_query(cursor, requete,
                          (telephone, mail, nom_artiste, prenom_artiste,
                           date_de_naissance, lieu_de_naissance, adresse,
                           numero_secu_sociale, cni, date_delivrance_cni,
                           date_expiration_cni, carte_reduction, genre_musical, nom_de_scene,
                           save_image(photo), id_artiste))
        else:
            requete = """
                UPDATE Artiste SET
                telephone = %s, mail = %s,
                nom_artiste = %s, prenom_artiste = %s,
                date_de_naissance = %s, lieu_naissance = %s, adresse = %s,
                securite_sociale = %s, cni = %s, date_delivrance_cni = %s,
                date_expiration_cni = %s, carte_reduction = %s,
                nom_style_musique = %s, nom_scene = %s
                WHERE id_artiste = %s
            """
            execute_query(cursor, requete,
                          (telephone, mail, nom_artiste, prenom_artiste,
                           date_de_naissance, lieu_de_naissance, adresse,
                           numero_secu_sociale, cni, date_delivrance_cni,
                           date_expiration_cni, carte_reduction,
                           genre_musical, nom_de_scene, id_artiste))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def confirmer_modif_salle(id_salle, nom, description, loge, nombre_place,
                          adresse, telephone, profondeur_scene, longueur_scene,
                          photo):
    try:
        cursor = get_cursor()

        if photo.filename != "":
            get_image(id_salle, "salle", photo)
            requete = """
                UPDATE Salle SET
                nom_salle = %s,
                description_salle = %s,
                loge = %s,
                nb_places = %s,
                adresse_salle = %s,
                telephone_salle = %s,
                profondeur_scene = %s,
                longueur_scene = %s,
                photo = %s,
                id_type_salle = %s
                WHERE id_salle = %s;
            """
            params = (nom, description, loge, nombre_place, adresse,
                      telephone, profondeur_scene, longueur_scene,
                      save_image(photo), id_salle)
            print(save_image(photo))
        else:
            requete = """
                UPDATE Salle SET
                nom_salle = %s,
                description_salle = %s,
                loge = %s,
                nb_places = %s,
                adresse_salle = %s,
                telephone_salle = %s,
                profondeur_scene = %s,
                longueur_scene = %s,
                id_type_salle = %s
                WHERE id_salle = %s;
            """
            params = (nom, description, loge, nombre_place, adresse, telephone,
                      profondeur_scene, longueur_scene, id_salle)

        execute_query(cursor, requete, params)
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def confirmer_modif_logement(id_logement, nom_etablissement, adresse,
                             nb_etoile, photo):
    try:
        get_image(id_logement, "logement", photo)
        cursor = get_cursor()
        requete = f"UPDATE Logement SET nom_etablissement = %s,adresse_ville_codepostal = %s,nb_etoile = %s, photo = %s WHERE id_logement = %s"
        execute_query(cursor, requete, (nom_etablissement, adresse, nb_etoile,
                                        save_image(photo), id_logement))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def remove_concert(id):
    try:
        # suppression dans avoir
        cursor = get_cursor()
        req = "DELETE FROM Avoir where id_concert= %s"
        cursor.execute(req, (id, ))
        close_cursor(cursor)
        # suppression dans besoin_equipement_artiste
        cursor = get_cursor()
        req = "DELETE FROM Besoin_equipement_artiste where id_concert= %s"
        cursor.execute(req, (id, ))
        close_cursor(cursor)
        # suppression dans loger
        cursor = get_cursor()
        req = "DELETE FROM Loger where id_concert= %s"
        cursor.execute(req, (id, ))
        close_cursor(cursor)
        # suppression dans participer
        cursor = get_cursor()
        req = "DELETE FROM Participer where id_concert= %s"
        cursor.execute(req, (id, ))
        close_cursor(cursor)
        # suppression du concert
        cursor = get_cursor()
        req = "DELETE FROM Concert where id_concert= %s"
        cursor.execute(req, (id, ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def remove_participer(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Participer where id_concert= %s and id_artiste = %s"
        cursor.execute(req, (
            id_concert,
            id_artiste,
        ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def remove_salle(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Salle where id_salle= %s"
        cursor.execute(req, (id, ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def remove_logement(id_logement):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Logement where id_logement= %s"
        cursor.execute(req, (id_logement, ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def remove_artiste(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Artiste where id_artiste= %s"
        cursor.execute(req, (id, ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def remvove_equipement(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Equipement where id_equipement= %s"
        cursor.execute(req, (id, ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def concerts_agenda1(heures, jour_voulu):
    agenda = {}

    for i in range(1, 8):
        agenda[i] = {}
        for heure in heures:
            agenda[i][heure] = []

    date_deb_semaine = jour_voulu - datetime.timedelta(
        days=jour_voulu.weekday())
    date_fin_semaine = date_deb_semaine + datetime.timedelta(days=6)

    for concert in concerts():
        date_deb = concert[2]
        date_fin = date_deb
        duree = concert[3]

        while date_deb.minute + duree > 59:
            date_fin += datetime.timedelta(hours=1)
            duree -= 60

        date_fin = date_fin.replace(minute=date_deb.minute + duree)

        if date_deb_semaine.date() <= date_deb.date() <= date_fin_semaine.date(
        ):
            a = agenda[date_deb.weekday() + 1]
            hour = date_deb.hour
            while hour not in a.keys():
                hour -= 1
            a[hour].append(concert[1])
        elif date_deb_semaine <= date_fin <= date_fin_semaine:
            pass

    return agenda


def concerts_agenda(heures=HEURES1, jour=JOUR_VOULU):
    """renvoie un agenda des concerts de la semaine du jour voulu"""
    #initialisation de l'agenda
    agenda = {}
    for i in range(1, 8):
        agenda[i] = {}
        for heure in heures:
            agenda[i][heure] = []
    #remplissage de l'agenda
    if len(heures) > 1:
        pas = heures[1] - heures[0]
    else:
        pas = 1
    if type(jour) == str:
        jour = datetime.datetime.strptime(jour, "%d-%m-%Y")
    for concert in concerts():
        date_debut = concert[2]
        if datetime.timedelta(days=-(jour.weekday() + 1)) < date_debut.replace(
                hour=0, minute=0) - jour < datetime.timedelta(
                    days=7 - (jour.weekday())):
            minutesC = date_debut.minute + concert[3] % 60
            trop = minutesC // 60
            minutesC -= trop * 60
            heuresC = date_debut.hour + concert[3] // 60 + trop
            depassement = 0
            if heuresC > 23:
                depassement = heuresC - 23
                heuresC = 23
            fin_concert = datetime.time(hour=heuresC, minute=minutesC)
            debut_concert = date_debut.time()
            for h in heures:
                # format 24h obligatoire
                if h + pas > 23:
                    fin_horaire = datetime.time(hour=h + pas - 1, minute=59)
                else:
                    fin_horaire = datetime.time(hour=h + pas)
                debut_horaire = datetime.time(hour=h)
                # ajouter le concert si il est dans l'intervalle horaire
                if not (debut_concert >= fin_horaire
                        or fin_concert < debut_horaire):
                    agenda[date_debut.weekday() + 1][h].append(
                        (concert[0], concert[1]))
            if depassement > 0:
                fin_depassement = datetime.time(hour=depassement,
                                                minute=minutesC)
                for h in heures:
                    if h + pas > 23:
                        fin_horaire = datetime.time(hour=h + pas - 1,
                                                    minute=59)
                    else:
                        fin_horaire = datetime.time(hour=h + pas)
                    debut_horaire = datetime.time(hour=h)
                    if fin_depassement > fin_horaire:
                        j = date_debut.weekday() + 2
                        if j < 8:
                            agenda[j][h].append((concert[0], concert[1]))
        elif datetime.timedelta(
                days=-(jour.weekday() + 1)) == date_debut.replace(
                    hour=0, minute=0) - jour:
            minutesC = date_debut.minute + concert[3] % 60
            trop = minutesC // 60
            minutesC -= trop * 60
            heuresC = date_debut.hour + concert[3] // 60 + trop
            depassement = 0
            if heuresC > 23:
                depassement = heuresC - 23
            fin_depassement = datetime.time(hour=depassement, minute=minutesC)
            for h in heures:
                # format 24h obligatoire
                if h + pas > 23:
                    fin_horaire = datetime.time(hour=h + pas - 1, minute=59)
                else:
                    fin_horaire = datetime.time(hour=h + pas)
                debut_horaire = datetime.time(hour=h)
                # ajouter le concert si il est dans l'intervalle horaire
                if fin_depassement > fin_horaire:
                    agenda[1][h].append((concert[0], concert[1]))
    return agenda

def get_type_salles():
    try:
        cursor = get_cursor()
        requete = "SELECT id_type,type_place_s FROM Type_Salle;"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None

def type_salle():
    try:
        cursor = get_cursor()
        requete = "SELECT id_salle,type_place_s FROM Type_Salle JOIN Salle ON Type_Salle.id_type = Salle.id_type_salle;"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        salle = {}
        for id_salle, type_place in info:
            salle[id_salle] = type_place
        return salle
    except Exception as e:
        print(e.args)
    return None


def add_artiste_concert(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        requete = "INSERT INTO Participer (id_concert, id_artiste) VALUES(%s, %s)"
        cursor.execute(requete, (
            id_concert,
            id_artiste,
        ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def get_concerts_artiste(id_artiste):
    try:
        cursor = get_cursor()
        requete = "SELECT Concert.* FROM Participer NATURAL JOIN Concert WHERE id_artiste = %s;"
        execute_query(cursor, requete, (id_artiste, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def get_equipement(id):
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Equipement where id_equipement= %s"
        cursor.execute(requete, (id, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None


def get_equipement_salle(id_salle):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement,nom_equipement,quantite FROM Posseder NATURAL JOIN Equipement WHERE id_salle = %s;"
        execute_query(cursor, requete, (id_salle, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def get_equipement_concert(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement,nom_equipement,quantite FROM Concert NATURAL JOIN Besoin_equipement_artiste NATURAL JOIN Equipement WHERE id_concert = %s and id_artiste = %s;"
        execute_query(cursor, requete, (
            id_concert,
            id_artiste,
        ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def categoriser_equipements1(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement, nom_equipement, quantite, quantite_posseder FROM Concert NATURAL JOIN Besoin_equipement_artiste NATURAL JOIN Equipement WHERE id_concert = %s and id_artiste = %s;"
        execute_query(cursor, requete, (
            id_concert,
            id_artiste,
        ))
        equipements = cursor.fetchall()
        close_cursor(cursor)

        possedes = [
            equipement for equipement in equipements
            if equipement[3] >= equipement[2]
        ]
        non_possedes = [
            equipement for equipement in equipements
            if equipement[3] < equipement[2]
        ]

        return possedes, non_possedes

    except Exception as e:
        print(e.args)
        return None, None


def categoriser_equipements(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement, nom_equipement, quantite, quantite_posseder FROM Concert NATURAL JOIN Besoin_equipement_artiste NATURAL JOIN Equipement WHERE id_concert = %s and id_artiste = %s;"
        execute_query(cursor, requete, (
            id_concert,
            id_artiste,
        ))
        equipements = cursor.fetchall()
        close_cursor(cursor)
        return equipements

    except Exception as e:
        print(e.args)
        return None, None


def equipements():
    equipements = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Equipement"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            equipements.append(i)
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return equipements


def get_equipements_concert(id_concert):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement,nom_equipement,quantite,quantite_posseder FROM Concert NATURAL JOIN Besoin_equipement_artiste NATURAL JOIN Equipement WHERE id_concert = %s;"
        execute_query(cursor, requete, (id_concert, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def get_id_quantite_equipements_concert(id_concert):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement, quantite FROM Concert NATURAL JOIN Besoin_equipement_artiste NATURAL JOIN Equipement WHERE id_concert = %s;"
        execute_query(cursor, requete, (id_concert, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def get_tous_equipements_concert(id_concert):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement, nom_equipement, IFNULL(quantite,0) FROM Equipement e NATURAL LEFT JOIN Concert NATURAL LEFT JOIN Besoin_equipement_artiste NATURAL LEFT JOIN Equipement WHERE id_concert = %s;"
        execute_query(cursor, requete, (id_concert, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def get_tous_equipements_salle(id_salle):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement, nom_equipement, IFNULL(quantite,0) FROM Equipement e NATURAL LEFT JOIN Salle NATURAL LEFT JOIN Posseder NATURAL LEFT JOIN Equipement WHERE id_salle = %s;"
        execute_query(cursor, requete, (id_salle, ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None


def get_equipements_disponible(id_concert, id_salle):
    equipements_concert = get_equipements_concert(id_concert)
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement,nom_equipement,quantite FROM Salle NATURAL JOIN Posseder NATURAL JOIN Equipement WHERE id_salle = %s;"
        execute_query(cursor, requete, (id_salle, ))
        infos = cursor.fetchall()
        close_cursor(cursor)
        equipements = []
        deja_vu = []
        for e in infos:
            if e[1] not in deja_vu:
                equipements.append(e)
                deja_vu.append(e[1])
        for e in equipements_concert:
            if e[1] not in deja_vu:
                equipements.append(e)
                deja_vu.append(e[1])
        return equipements
    except Exception as e:
        print(e.args)
    return None


def save_artiste(id_artiste,
                 nom_artiste,
                 prenom_artiste,
                 mail,
                 telephone,
                 date_de_naissance,
                 lieu_de_naissance,
                 adresse,
                 securite_sociale,
                 cni,
                 date_delivrance_cni,
                 date_expiration_cni,
                 carte_reduction,
                 genre_musique,
                 nom_scene,
                 conge_spectacle="Non"):
    try:
        cursor = get_cursor()
        req = "INSERT INTO Artiste (id_artiste, nom_artiste, prenom_artiste, mail, telephone, date_de_naissance, lieu_naissance, adresse, securite_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction, nom_style_musique, nom_scene,conge_spectacle) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
        cursor.execute(
            req,
            (id_artiste, nom_artiste, prenom_artiste, mail, telephone,
             date_de_naissance, lieu_de_naissance, adresse, securite_sociale,
             cni, date_delivrance_cni, date_expiration_cni, carte_reduction,
             genre_musique, nom_scene, conge_spectacle))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)


def save_equipement_concert(id_concert, id_equipement, quantite):
    try:
        cursor = get_cursor()
        requete = "UPDATE Besoin_equipement_artiste SET quantite_posseder = %s WHERE id_concert = %s and id_equipement = %s;"
        execute_query(cursor, requete, (
            quantite,
            id_concert,
            id_equipement,
        ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def save_necessaire_concert(id_concert,
                            id_equipement,
                            quantite,
                            id_artiste,
                            ancienne_quantite=0):
    try:
        if quantite == 0:
            cursor = get_cursor()
            requete = "DELETE FROM Besoin_equipement_artiste WHERE id_concert = %s and id_equipement = %s;"
            execute_query(cursor, requete, (
                id_concert,
                id_equipement,
            ))
            db.commit()
            close_cursor(cursor)
        elif ancienne_quantite > 0:
            cursor = get_cursor()
            requete = "UPDATE Besoin_equipement_artiste SET quantite = %s WHERE id_concert = %s and id_equipement = %s;"
            execute_query(cursor, requete, (
                quantite,
                id_concert,
                id_equipement,
            ))
            db.commit()
            close_cursor(cursor)
        else:
            cursor = get_cursor()
            requete = "INSERT INTO Besoin_equipement_artiste (id_concert, id_equipement, id_artiste, quantite, quantite_posseder) VALUES(%s, %s, %s, %s, %s)"
            execute_query(cursor, requete, (
                id_concert,
                id_equipement,
                id_artiste,
                quantite,
                0,
            ))
            db.commit()
            close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def save_equipement_salle(id_salle,
                          id_equipement,
                          quantite,
                          ancienne_quantite=0):
    try:
        if quantite == 0:
            cursor = get_cursor()
            requete = "DELETE FROM Posseder WHERE id_salle = %s and id_equipement = %s;"
            execute_query(cursor, requete, (
                id_salle,
                id_equipement,
            ))
            db.commit()
            close_cursor(cursor)
        elif ancienne_quantite > 0:
            cursor = get_cursor()
            requete = "UPDATE Posseder SET quantite = %s WHERE id_salle = %s and id_equipement = %s;"
            execute_query(cursor, requete, (
                quantite,
                id_salle,
                id_equipement,
            ))
            db.commit()
            close_cursor(cursor)
        else:
            cursor = get_cursor()
            requete = "INSERT INTO Posseder (id_salle, id_equipement, quantite) VALUES(%s, %s, %s)"
            execute_query(cursor, requete, (
                id_salle,
                id_equipement,
                quantite,
            ))
            db.commit()
            close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def get_logement_artiste(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        requete = "SELECT id_logement, nom_etablissement, nb_nuit FROM Logement NATURAL JOIN Loger WHERE id_artiste = %s AND id_concert=%s;"
        execute_query(cursor, requete, (
            id_artiste,
            id_concert,
        ))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None


def supprimer_logement_artiste(id_concert, id_artiste):
    try:
        cursor = get_cursor()
        requete = "DELETE FROM Loger WHERE id_artiste = %s AND id_concert=%s;"
        execute_query(cursor, requete, (
            id_artiste,
            id_concert,
        ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None


def add_logement_artiste(id_concert, id_artiste, id_logement, nb_nuit):
    try:
        cursor = get_cursor()
        requete = "INSERT INTO Loger (id_artiste, id_concert, id_logement, nb_nuit) VALUES(%s, %s, %s, %s)"
        execute_query(cursor, requete, (
            id_artiste,
            id_concert,
            id_logement,
            nb_nuit,
        ))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None

def get_type_salle(id_salle):
    try:
        cursor = get_cursor()
        requete = "SELECT id_type, type_place_s FROM Type_Salle JOIN Salle ON Salle.id_type_salle = Type_Salle.id_type WHERE id_salle = %s;"
        execute_query(cursor, requete, (id_salle,))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def confirmer_modif_equipement(id_equipement, nom_equipement):
    try:
        cursor = get_cursor()
        requete = "UPDATE Equipement SET nom_equipement = %s WHERE id_equipement = %s;"
        execute_query(cursor, requete, (nom_equipement, id_equipement))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None
