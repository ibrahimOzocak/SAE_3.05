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