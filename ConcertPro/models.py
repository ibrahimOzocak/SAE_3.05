import mysql.connector
from PIL import Image
from io import BytesIO
import datetime
import io

HEURES1 = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
PAS1 = 1
JOUR_VOULU = datetime.datetime.now()
HEURES2 = [8, 10, 12, 14, 16, 18, 20, 22]
PAS2 = 2

db = mysql.connector.connect(
    host="servinfo-maria",user = "sevellec", password = "sevellec", database = "DBsevellec"
)

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
                get_image(int(i[0]),"concerts", i[-1])
        return infos
    except Exception as e:
        print(e.args)

def save_concert(id, nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert,photo):
    try:
        cursor = get_cursor()
        req = "INSERT INTO Concert (id_concert,nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert, photo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(req, (id,nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert,save_image(photo)))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None

def save_salle(id, nom_salle,nb_places,profondeur_scene,longueur_scene,telephone_salle,type_place,description_salle,photo,adresse_salle,loge,acces_pmr):
    try:
        cursor = get_cursor()
        req = "INSERT INTO Salle (id_salle, id_type_salle, loge, nom_salle, nb_places, profondeur_scene, longueur_scene, description_salle,adresse_salle,telephone_salle, accueil_pmr, photo) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(req, (id, get_id_type_salles(type_place),loge,nom_salle,nb_places, profondeur_scene,longueur_scene,description_salle,adresse_salle,telephone_salle,acces_pmr,save_image(photo)))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def save_image(photo):
    try:
        if photo.filename != '':
            image_data = photo.read()
            image_bytesio = io.BytesIO(image_data)
            blob = image_bytesio.read()
            return blob
    except Exception as e:
        print(e.args)
    return None
    
def get_image(id_value, repesitory_name, image_data):
    if id_value is None:
        return
    try:
        if image_data is None:
            print("no image data")
            return
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')
        nom_fichier = "ConcertPro/static/images/"+repesitory_name+"/"+str(id_value)+".jpg"
        image.save(nom_fichier)
    except Exception as e:
        print(e.args)
    
# fonctions utiles pour les templates
def get_concert(id):
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where id_concert= %s"
        cursor.execute(requete, (id,))
        info = cursor.fetchall()
        if info[0][-1] is not None:
            get_image(int(info[0][0]),"concerts", info[0][-1])
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_salle(id):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Salle WHERE id_salle = %s"
        cursor.execute(request, (id,))
        info = cursor.fetchall()
        if info[0][-2] is not None:
            get_image(int(info[0][0]),"salle", info[0][-2])
        close_cursor(cursor)
        return info[0] if info else None
    except Exception as e:
        print(e.args)
        return None


def get_logement(id_logement):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Logement where id_logement = %s"
        cursor.execute(request, (id_logement,))
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
        cursor.execute(request, (id,))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_id_type_salles(nom):
    try:
        cursor = get_cursor()
        request = "SELECT id_type FROM Type_Salle where type_place_s= %s"
        cursor.execute(request, (nom,))
        info = cursor.fetchall()
        close_cursor(cursor)
        if info == []:
            # à la place rajouter le type dans la base de données
            return 1
        return info[0][0]
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
                get_image(int(i[0]), "concerts", i[-1])
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
                get_image(int(i[0]), "concerts", i[-1])
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
            if i[-1] is not None:
                get_image(int(i[0]), "salle", i[-1])
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
                get_image(i[0], "logement", i[-1])
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
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def get_id_artiste_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_artiste) FROM Artiste"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def get_id_salle_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_salle) FROM Salle"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def get_id_logement_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_logement) FROM Logement"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def get_id_equipement_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_equipement) FROM Equipement"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def get_id_type_salle_max():
    try:
        cursor = get_cursor()
        requete = "SELECT MAX(id_type) FROM Type_Salle"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0][0]
    except Exception as e:
        print(e.args)
    return None

def confirmer_modif_concert(id_concert, nom_concert, date_heure_concert, duree_concert, description_concert):
    try:
        cursor = get_cursor()
        requete = f"UPDATE Concert SET nom_concert = %s, date_heure_concert = %s, duree_concert = %s, description_concert = %s WHERE id_concert = %s"
        execute_query(cursor, requete, (nom_concert, date_heure_concert, duree_concert, description_concert, id_concert))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None

def confirmer_modif_artiste(id_artiste, nom_artiste, nom_de_scene, mail, telephone, date_de_naissance, lieu_de_naissance,
        adresse, numero_secu_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction):
    try:
        cursor = get_cursor()
        requete = f"UPDATE Artiste SET telephone = %s, mail = %s,nom_artiste = %s,date_de_naissance = %s,lieu_naissance = %s,adresse = %s,securite_sociale = %s,cni = %s,date_delivrance_cni = %s,date_expiration_cni = %s,carte_reduction = %s,nom_scene = %s WHERE id_artiste = %s"
        execute_query(cursor, requete, (telephone, mail, nom_artiste, date_de_naissance, lieu_de_naissance, adresse, numero_secu_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction, nom_de_scene,id_artiste))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None

def confirmer_modif_salle(id_salle, nom, description, loge, nombre_place, adresse, telephone, profondeur_scene, longueur_scene):
    try:
        cursor = get_cursor()
        requete = f"UPDATE Salle SET nom_salle = %s, description_salle = %s, loge = %s, nb_places = %s, adresse_salle = %s, telephone_salle = %s, profondeur_scene = %s, longueur_scene = %s WHERE id_salle = %s"
        execute_query(cursor, requete, (nom, description, loge, nombre_place, adresse, telephone, profondeur_scene, longueur_scene, id_salle))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return None

def confirmer_modif_logement(id_logement, nom_etablissement, adresse, nb_etoile):
    try:
        cursor = get_cursor()
        requete = f"UPDATE Logement SET nom_etablissement = %s,adresse_ville_codepostal = %s,nb_etoile = %s WHERE id_logement = %s"
        execute_query(cursor, requete, (nom_etablissement, adresse, nb_etoile, id_logement))
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
        cursor.execute(req, (id,))
        close_cursor(cursor)
        # suppression dans besoin_equipement_artiste
        cursor = get_cursor()
        req = "DELETE FROM Besoin_equipement_artiste where id_concert= %s"
        cursor.execute(req, (id,))
        close_cursor(cursor)
        # suppression dans loger
        cursor = get_cursor()
        req = "DELETE FROM Loger where id_concert= %s"
        cursor.execute(req, (id,))
        close_cursor(cursor)
        # suppression dans participer
        cursor = get_cursor()
        req = "DELETE FROM Participer where id_concert= %s"
        cursor.execute(req, (id,))
        close_cursor(cursor)
        # suppression du concert
        cursor = get_cursor()
        req = "DELETE FROM Concert where id_concert= %s"
        cursor.execute(req, (id,))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_salle(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Salle where id_salle= %s"
        cursor.execute(req, (id,))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_logement(id_logement):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Logement where id_logement= %s"
        cursor.execute(req, (id_logement,))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_artiste(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Artiste where id_artiste= %s"
        cursor.execute(req, (id,))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
def remvove_equipement(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Equipement where id_equipement= %s"
        cursor.execute(req, (id,))
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def concerts_agenda1(heures, jour_voulu):
    agenda = {}

    for i in range(1,8):
        agenda[i] = {}
        for heure in heures:
            agenda[i][heure] = []

    date_deb_semaine = jour_voulu - datetime.timedelta(days=jour_voulu.weekday())
    date_fin_semaine = date_deb_semaine + datetime.timedelta(days=6)

    for concert in concerts():
        date_deb = concert[2]
        date_fin = date_deb
        duree = concert[3]
        
        while date_deb.minute+duree > 59:
            date_fin += datetime.timedelta(hours=1)  
            duree -= 60
        
        date_fin = date_fin.replace(minute=date_deb.minute+duree)
                
        if date_deb_semaine.date() <= date_deb.date() <= date_fin_semaine.date():
            a = agenda[date_deb.weekday()+1]
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
    for i in range(1,8):
        agenda[i] = {}
        for heure in heures:
            agenda[i][heure] = []
    #remplissage de l'agenda
    if len(heures) > 1:
        pas = heures[1]-heures[0]
    else:
        pas = 1
    if type(jour) == str:
        jour = datetime.datetime.strptime(jour, "%d-%m-%Y")
    for concert in concerts():
        date_debut = concert[2]
        if datetime.timedelta(days=-(jour.weekday()+1))<date_debut.replace(hour=0, minute=0)-jour<datetime.timedelta(days=7-(jour.weekday())):
            minutesC = date_debut.minute+concert[3]%60
            trop = minutesC//60
            minutesC-=trop*60
            heuresC = date_debut.hour+concert[3]//60+trop
            depassement = 0
            if heuresC > 23:
                depassement = heuresC-23
                heuresC = 23
            fin_concert = datetime.time(hour=heuresC, minute=minutesC)
            debut_concert = date_debut.time()
            for h in heures:
                # format 24h obligatoire
                if h+pas > 23:
                    fin_horaire = datetime.time(hour=h+pas-1, minute=59)
                else:
                    fin_horaire = datetime.time(hour=h+pas)
                debut_horaire = datetime.time(hour=h)
                # ajouter le concert si il est dans l'intervalle horaire
                if not(debut_concert >= fin_horaire or fin_concert < debut_horaire):
                    agenda[date_debut.weekday()+1][h].append((concert[0],concert[1]))
            if depassement > 0:
                fin_depassement = datetime.time(hour=depassement, minute=minutesC)
                for h in heures:
                    if h+pas > 23:
                        fin_horaire = datetime.time(hour=h+pas-1, minute=59)
                    else:
                        fin_horaire = datetime.time(hour=h+pas)
                    debut_horaire = datetime.time(hour=h)
                    if fin_depassement > fin_horaire:
                        j = date_debut.weekday()+2
                        if j < 8:
                            agenda[j][h].append((concert[0],concert[1]))
        elif datetime.timedelta(days=-(jour.weekday()+1))==date_debut.replace(hour=0, minute=0)-jour:
            minutesC = date_debut.minute+concert[3]%60
            trop = minutesC//60
            minutesC-=trop*60
            heuresC = date_debut.hour+concert[3]//60+trop
            depassement = 0
            if heuresC > 23:
                depassement = heuresC-23
            fin_depassement = datetime.time(hour=depassement, minute=minutesC)
            for h in heures:
                # format 24h obligatoire
                if h+pas > 23:
                    fin_horaire = datetime.time(hour=h+pas-1, minute=59)
                else:
                    fin_horaire = datetime.time(hour=h+pas)
                debut_horaire = datetime.time(hour=h)
                # ajouter le concert si il est dans l'intervalle horaire
                if fin_depassement > fin_horaire:
                    agenda[1][h].append((concert[0],concert[1]))
    return agenda

def type_salle():
    try:
        cursor = get_cursor()
        requete = "SELECT type_place_s FROM Type_Salle"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None

def get_concerts_artiste(id_artiste):
    try:
        cursor = get_cursor()
        requete = "SELECT Concert.* FROM Participer NATURAL JOIN Concert WHERE id_artiste = %s;"
        execute_query(cursor, requete, (id_artiste,))
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
        cursor.execute(requete, (id,))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_equipement_salle(id_salle):
    try:
        cursor = get_cursor()
        requete = "SELECT id_equipement,nom_equipement,quantite FROM Salle NATURAL JOIN Posseder NATURAL JOIN Equipement WHERE id_salle = %s;"
        execute_query(cursor, requete, (id_salle,))
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
        execute_query(cursor, requete, (id_concert, id_artiste,))
        info = cursor.fetchall()
        close_cursor(cursor)
        return info
    except Exception as e:
        print(e.args)
    return None

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