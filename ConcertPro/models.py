import mysql.connector
from PIL import Image
from io import BytesIO
from flask import Response

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
                get_image(int(i[0]))
        return infos
    except Exception as e:
        print(e.args)

def save_image(chemin_img):
    try:
        cursor = get_cursor()
        with open(chemin_img, 'rb') as image_file:
            image_data = image_file.read()

        update_query = "UPDATE Concert SET photo = %s WHERE id_concert = %s"
        execute_query(cursor, update_query, (image_data, 1))
        close_cursor(cursor)
        db.commit()
        return "Image sauvegardée avec succès"
    except Exception as e:
        return "Erreur lors de la sauvegarde de l'image"

if __name__ == '__main__':
    save_image("/home/iut45/Etudiants/o22202357/WinHome/analyse/Diagramme_de_cas_dutilisations.png")

def get_image(id_concert):
    if id_concert is None:
        return
    try:
        cursor = get_cursor()
        select_query = "SELECT photo FROM Concert WHERE id_concert = %s"
        cursor.execute(select_query, (id_concert,))
        image_data = cursor.fetchone()[0]
        if image_data is None:
            return
        image = Image.open(BytesIO(image_data))
        image = image.convert('RGB')
        nom_fichier = "ConcertPro/static/images/"+str(id_concert)+".jpg"
        image.save(nom_fichier)
        close_cursor(cursor)
    except Exception as e:
        return "Erreur lors de la récupération de l'image"
    
# fonctions utiles pour les templates
def get_concert(nom):
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where nom_concert='"+nom+"'"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_salle(nom):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Salle where nom_salle='"+nom+"'"
        cursor.execute(request)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_logement(nom_etablissement):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Logement where nom_etablissement='"+nom_etablissement+"'"
        cursor.execute(request)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_artiste(nom):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Artiste where nom_artiste='"+nom+"'"
        cursor.execute(request)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_id_type_salles(nom):
    try:
        cursor = get_cursor()
        request = "SELECT id_type FROM Type_Salle where type_place_s='"+nom+"'"
        cursor.execute(request)
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
    prochains_concerts = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where date_heure_concert < CURDATE()"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            prochains_concerts.append(i)
        close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return prochains_concerts

def concerts():
    concerts = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            concerts.append(i)
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

def remove_concert(nom):
    concert = mo.get_concert(nom)
    try:
        cursor = mo.get_cursor()
        req = "DELETE FROM Concert where id_concert="+str(concert[0])
        cursor.execute(req)
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_salle(nom):
    salle = mo.get_salle(nom)
    try:
        cursor = mo.get_cursor()
        req = "DELETE FROM Salle where id_salle="+str(salle[0])
        cursor.execute(req)
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_logement(nom_etablissement):
    logement = mo.get_logement(nom_etablissement)
    try:
        cursor = mo.get_cursor()
        req = "DELETE FROM Logement where id_logement="+str(logement[0])
        cursor.execute(req)
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_artiste(nom):
    artiste = mo.get_artiste(nom)
    try:
        cursor = mo.get_cursor()
        req = "DELETE FROM Artiste where id_artiste="+str(artiste[0])
        cursor.execute(req)
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)

def concerts_agenda(heures=HEURES1,pas=PAS1,jour_voulu=JOUR_VOULU):
    """renvoie un agenda des concerts de la semaine du jour voulu"""
    #initialisation de l'agenda
    agenda = {}
    for i in range(1,8):
        agenda[i] = {}
        for heure in heures:
            agenda[i][heure] = []
    #remplissage de l'agenda
    jour = jour_voulu
    if type(jour) == str:
        jour = datetime.datetime.strptime(jour, "%d-%m-%Y")
    for concert in mo.concerts():
        # if datetime.timedelta(days=-(jour.weekday()+1))<concert["date_debut"]-jour<datetime.timedelta(days=7-(jour.weekday()+1)+1):
        #     for h in heures:
        #         fin_horaire = h+pas
        #         # format 24h obligatoire
        #         if fin_horaire > 23:
        #             fin_horaire = datetime.time(hour=h+pas-1, minute=59)
        #         else:
        #             fin_horaire = datetime.time(hour=h+pas)
        #         debut_horaire = datetime.time(hour=h)
        #         minutesC = (concert["heure_debut"].minute+concert["minute_duree"])%60
        #         heuresC = concert["heure_debut"].hour+concert["heure_duree"]+(concert["heure_debut"].minute+concert["minute_duree"])//60
        #         fin_concert = datetime.time(hour=heuresC, minute=minutesC)
        #         debut_concert = concert["heure_debut"]
        #         # ajouter le concert si il est dans l'intervalle horaire
        #         if not(debut_concert >= fin_horaire or fin_concert <= debut_horaire):
        #             agenda[concert["date_debut"].weekday()+1][h].append(concert["nom"])
        pass
    return agenda
