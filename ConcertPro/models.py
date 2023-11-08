import mysql.connector
from PIL import Image
from io import BytesIO
import datetime

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
                get_image(int(i[0]))
        return infos
    except Exception as e:
        print(e.args)

def save_image(chemin_img, id_value, table):
    try:
        cursor = get_cursor()
        with open(chemin_img, 'rb') as image_file:
            image_data = image_file.read()

        update_query = f"UPDATE {table} SET photo = {image_data} WHERE id_concert = {id_value}"
        execute_query(cursor, update_query)
        close_cursor(cursor)
        db.commit()
        return "Image sauvegardée avec succès"
    except Exception as e:
        return "Erreur lors de la sauvegarde de l'image"

if __name__ == '__main__':
    save_image("/home/iut45/Etudiants/o22202357/Bureau/images.jpeg", 1, "Concert")
    save_image("/home/iut45/Etudiants/o22202357/Bureau/images2.jpeg", 2, "Concert")
    save_image("/home/iut45/Etudiants/o22202357/Bureau/images4.png", 3, "Concert")

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
        nom_fichier = "ConcertPro/static/images/concerts/"+str(id_concert)+".jpg"
        image.save(nom_fichier)
        close_cursor(cursor)
    except Exception as e:
        return "Erreur lors de la récupération de l'image"
    
# fonctions utiles pour les templates
def get_concert(id):
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where id_concert='"+id+"'"
        cursor.execute(requete)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_salle(id):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Salle where id_salle='"+id+"'"
        cursor.execute(request)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_logement(id_logement):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Logement where id_logement='"+id_logement+"'"
        cursor.execute(request)
        info = cursor.fetchall()
        close_cursor(cursor)
        return info[0]
    except Exception as e:
        print(e.args)
    return None

def get_artiste(id):
    try:
        cursor = get_cursor()
        request = "SELECT * FROM Artiste where id_artiste='"+id+"'"
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
    historique_concerts = []
    try:
        cursor = get_cursor()
        requete = "SELECT * FROM Concert where date_heure_concert < NOW()"
        cursor.execute(requete)
        info = cursor.fetchall()
        for i in info:
            historique_concerts.append(i)
            if i[-1] is not None:
                get_image(int(i[0]))
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

def remove_concert(id):
    try:
        # suppression dans avoir
        cursor = get_cursor()
        req = "DELETE FROM Avoir where id_concert="+str(id)
        cursor.execute(req)
        close_cursor(cursor)
        # suppression dans besoin_equipement_artiste
        cursor = get_cursor()
        req = "DELETE FROM Besoin_equipement_artiste where id_concert="+str(id)
        cursor.execute(req)
        close_cursor(cursor)
        # suppression dans loger
        cursor = get_cursor()
        req = "DELETE FROM Loger where id_concert="+str(id)
        cursor.execute(req)
        close_cursor(cursor)
        # suppression dans participer
        cursor = get_cursor()
        req = "DELETE FROM Participer where id_concert="+str(id)
        cursor.execute(req)
        close_cursor(cursor)
        # suppression du concert
        cursor = get_cursor()
        req = "DELETE FROM Concert where id_concert="+str(id)
        cursor.execute(req)
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_salle(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Salle where id_salle="+str(id)
        cursor.execute(req)
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_logement(id_logement):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Logement where id_logement="+str(id_logement)
        cursor.execute(req)
        db.commit()
        close_cursor(cursor)
    except Exception as e:
        print(e.args)

def remove_artiste(id):
    try:
        cursor = get_cursor()
        req = "DELETE FROM Artiste where id_artiste="+str(id)
        cursor.execute(req)
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
    if len(heures) < 1:
        pas = heures[1]-heures[0]
    else:
        pas = 1
    if type(jour) == str:
        jour = datetime.datetime.strptime(jour, "%d-%m-%Y")
    for concert in concerts():
        date_debut = concert[2]
        if datetime.timedelta(days=-(jour.weekday()+1))<date_debut.replace(hour=0, minute=0)-jour<datetime.timedelta(days=7-(jour.weekday())):
            for h in heures:
                # format 24h obligatoire
                if h+pas > 23:
                    fin_horaire = datetime.time(hour=h+pas-1, minute=59)
                else:
                    fin_horaire = datetime.time(hour=h+pas)
                debut_horaire = datetime.time(hour=h)
                minutesC = date_debut.minute+concert[3]%60
                trop = minutesC//60
                minutesC-=trop*60
                heuresC = date_debut.hour+concert[3]//60+trop

                fin_concert = datetime.time(hour=heuresC, minute=minutesC)
                debut_concert = date_debut.time()
                # ajouter le concert si il est dans l'intervalle horaire
                if not(debut_concert >= fin_horaire or fin_concert <= debut_horaire):
                    agenda[date_debut.weekday()+1][h].append((concert[0],concert[1]))
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

