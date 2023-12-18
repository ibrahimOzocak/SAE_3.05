from flask import redirect, render_template, request, url_for
import folium
from .app import app, db
import datetime
from . import models as mo
import requests
import json

HEURES_DECALAGE_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
HEURES_DECALAGE_2 = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]

# accueil
@app.route('/')
def accueil():
    """page d'accueil"""
    jour = datetime.datetime.now()
    agenda = mo.concerts_agenda(HEURES_DECALAGE_2,jour)
    lundi = (jour + datetime.timedelta(days=-(jour.weekday()+1)) + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    dimanche = (jour + datetime.timedelta(days=7-(jour.weekday()+1))).replace(hour=23, minute=59, second=59, microsecond=0)
    return render_template(
        "accueil.html",
        concerts=mo.prochains_concerts(),
        agenda=agenda,
        heures=HEURES_DECALAGE_2,
        date_lundi=lundi.strftime("%d-%m-%Y"),
        date_dimanche=dimanche.strftime("%d-%m-%Y")
    )

@app.route('/plan_feu')
def plan_feu():
    """page du plan feu"""
    return render_template(
        "plan_feu.html"
    )


@app.template_filter('str')
def string_filter(value):
    return str(value)

# concert
@app.route('/creer_concert')
def creer_concert():
    """page de création de concert"""
    return render_template(
        "creer_concert.html",
        artistes=mo.artistes(),
        salles=mo.salles(),
        types = mo.type_salle()
    )

@app.route('/voir_prochains_concerts')
def voir_prochains_concerts():
    """page qui affiche les concerts à venir"""
    return render_template(
        "voir_prochains_concerts.html",
        concerts=mo.prochains_concerts()
    )
    

@app.route('/historique_concert')
def historique_concerts():
    """page qui affiche les concerts passés"""
    return render_template(
        "historique_concerts.html",
        concerts = mo.historique_concerts()
    )

@app.route('/save_concert', methods=("POST",))
def save_concert():
    """sauvegarde d'un concert"""
    nom_concert = request.form['titre']
    date_debut = datetime.datetime.strptime(request.form['date_debut'], "%Y-%m-%d")
    heure_debut = datetime.datetime.strptime(request.form['heure_debut'], "%H:%M").time()
    date_heure_concert = datetime.datetime.combine(date_debut, heure_debut)
    heure_duree = datetime.datetime.strptime(request.form['duree'], "%H:%M").time().hour
    minute_duree = datetime.datetime.strptime(request.form['duree'], "%H:%M").time().minute
    duree_concert = heure_duree*60 + minute_duree
    id_artiste = request.form['artiste']
    id_salle = request.form['salle']
    description_concert = request.form['description']
    photo = request.files['image']
    id = mo.get_id_concert_max()+1
    
    mo.save_concert(id, nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert,photo)
    
    return redirect(url_for('concert', id=id))

@app.route('/concert/<id>')
def concert(id):
    """page pour le concert <id>"""
    concert = mo.get_concert(id)
    salle = mo.get_salle(concert[5])
    artiste = mo.get_artiste(concert[4])
    possedes, non_possedes = mo.categoriser_equipements(id, artiste[0])
    print(possedes)
    print(non_possedes)
    return render_template(
        "concert.html",
        concert=concert,
        salle = salle,
        artiste = artiste,
        possedes = possedes,
        non_possedes = non_possedes
    )

@app.route('/concert/<id>/supprimer')
def supprimer_concert(id):
    """supprime le concert <id>"""
    mo.remove_concert(id)
    return redirect(url_for('voir_prochains_concerts'))

@app.route('/concert/<id_concert>/modifier')
def modifier_concert(id_concert):
    """modifier le concert <id_concert>"""
    concert = mo.get_concert(id_concert)
    return render_template(
        "modifier_concert.html",
        concert=concert
    )

@app.route('/modifier_concert/<id_concert>/<nom_concert>', methods=("POST",))
def confirmer_modif_concert(id_concert, nom_concert):
    """sauvegarde d'un concert"""
    nom_concert= request.form['nom_concert']
    date_heure_concert = request.form['date_heure_concert']
    duree_concert = request.form['duree_concert']
    description_concert = request.form['description_concert']
    photo = request.files['image']
    
    mo.confirmer_modif_concert(id_concert,nom_concert, date_heure_concert, duree_concert, description_concert,photo)
    
    return redirect(url_for('concert', id=id_concert))

# salle
@app.route('/ajout_nouvelle_salle')
def ajout_nouvelle_salle():
    """page de création de salle"""
    return render_template(
        "ajout_nouvelle_salle.html",
        types = mo.type_salle()
    )

@app.route('/voir_salles')
def voir_salles():
    """page qui affiche les salles"""
    return render_template(
            "voir_salles.html",
            salles=mo.salles()
        )

@app.route('/salle/<id>')
def salle(id):
    """page pour la salle <id>"""
    salle = mo.get_salle(id)
    equipement = mo.get_equipement_salle(id)
    return render_template(
        "salle.html",
        salle=salle,
        equipement = equipement
    )

@app.route('/save_salle', methods=("POST",))
def save_salle():
    """sauvegarde d'une salle"""
    nom_salle = request.form['titre']
    nb_places = request.form['place']
    profondeur_scene = request.form['profondeur']
    longueur_scene = request.form['longueur']
    adresse_salle = request.form['adresse']
    telephone_salle = request.form['telephone']
    code_postal_salle = request.form['postalville']
    type_place = request.form['type_salle']
    description_salle = request.form['description']
    photo = request.files['image']
    
    # nomequipement 
    # quantitedispo 
    
    
    adresse_salle = adresse_salle + ", " + code_postal_salle
    loge = ""
    acces_pmr = ""
    
    for elem in request.form:
        if elem == "loge":
            loge = "oui"
        elif elem == "accueilpmr":
            acces_pmr = "oui"
    if loge == "":
        loge = "non"
    if acces_pmr == "":
        acces_pmr = "non"
    id = mo.get_id_salle_max()+1
    
    mo.save_salle(id, nom_salle,nb_places,profondeur_scene,longueur_scene,telephone_salle,type_place,description_salle,photo,adresse_salle,loge,acces_pmr)
    
    return redirect(url_for('salle', id=id))

@app.route('/salle/<id_salle>/supprimer')
def supprimer_salle(id_salle):
    """supprime la salle <id_salle>"""
    mo.remove_salle(id_salle)
    return redirect(url_for('voir_salles'))

# artiste
@app.route('/ajout_artiste')
def ajout_artiste():
    """page d'ajout d'un artiste"""
    return render_template(
        "ajout_artiste.html"
    )

@app.route('/voir_artistes')
def voir_artistes():
    try:
        cursor = mo.get_cursor()
        request = "SELECT * FROM Artiste"
        cursor.execute(request)
        info = cursor.fetchall()
        mo.close_cursor(cursor)
        return render_template(
            "voir_artistes.html",
            artistes=info
        )
    except Exception as e:
        print(e.args)
        return render_template(
            "error.html",
            error_message="An error occurred while retrieving data from the database."
        )

@app.route('/artiste/<id_artiste>')
def artiste(id_artiste):
    """page de l'artiste <id_artiste>"""
    artiste = mo.get_artiste(id_artiste)
    concerts = mo.get_concerts_artiste(id_artiste)
    return render_template(
        "artiste.html",
        artiste=artiste,
        concerts=concerts
    )

@app.route('/confirmer_artiste/<id_artiste>/<nom_artiste>', methods=("POST",))
def confirmer_modif_artiste(id_artiste, nom_artiste):
    """sauvegarde d'un artiste"""
    nom_de_scene = request.form['nom_de_scene']
    mail = request.form['mail']
    telephone = request.form['telephone']
    date_de_naissance = request.form['date_de_naissance']
    lieu_de_naissance = request.form['lieu_de_naissance']
    adresse = request.form['adresse']
    numero_secu_sociale = request.form['numero_secu_sociale']
    cni = request.form['cni']
    date_delivrance_cni = request.form['date_delivrance_cni']
    date_expiration_cni = request.form['date_expiration_cni']
    carte_reduction = request.form['carte_de_reduction']
    photo = request.files['image']
    mo.confirmer_modif_artiste(id_artiste, nom_artiste, nom_de_scene, mail, telephone, date_de_naissance, lieu_de_naissance,
        adresse, numero_secu_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction,photo)
    return redirect(url_for('artiste', id_artiste=id_artiste))

@app.route('/confirmer_salle/<id_salle>/<nom_salle>', methods=("POST",))
def confirmer_modif_salle(id_salle, nom_salle):
    """sauvegarde d'un artiste"""
    nom = request.form["nom"]
    description = request.form['description']
    loge = request.form['loge']
    nombre_place = request.form['nombre de places']
    adresse = request.form['adresse']
    telephone = request.form['telephone']
    profondeur_scene = request.form['profondeur scene']
    longueur_scene = request.form['longueur scene']
    photo = request.files['image']
    mo.confirmer_modif_salle(id_salle, nom, description, loge, nombre_place, adresse, telephone, profondeur_scene, longueur_scene,photo)
    return redirect(url_for('salle', id=id_salle))
    
@app.route('/artiste/<id_artiste>/modifier')
def modifier_artiste(id_artiste):
    """page de l'artiste <id_artiste>"""
    artiste = mo.get_artiste(id_artiste)
    return render_template(
        "modifier_artiste.html",
        artiste=artiste
    )

@app.route('/salle/<id_salle>/modifier')
def modifier_salle(id_salle):
    """page de la salle <id_salle>"""
    salle = mo.get_salle(id_salle)
    return render_template(
        "modifier_salle.html",
        salle=salle
    )

@app.route('/save_artiste', methods=("POST",))
def save_artiste():
    """sauvegarde d'un artiste"""
    nom_artiste = request.form['nom']
    prenom_artiste = request.form['prenom']
    mail = request.form['mail']
    telephone = request.form['telephone']
    date_de_naissance = datetime.datetime.strptime(request.form['date_naissance'], "%Y-%m-%d")
    lieu_de_naissance = request.form['lieu_naissance']
    adresse = request.form['adresse']
    securite_sociale = request.form['num_secu_sociale']
    cni = request.form['cni']
    date_delivrance_cni = datetime.datetime.strptime(request.form['date_delivrance'], "%Y-%m-%d")
    date_expiration_cni = datetime.datetime.strptime(request.form['date_expiration'], "%Y-%m-%d")
    carte_reduction = request.form['carte_train']
    id_artiste = mo.get_id_artiste_max()+1
    try:
        cursor = mo.get_cursor()
        req = "INSERT INTO Artiste (id_artiste, nom_artiste, prenom_artiste, mail, telephone, date_de_naissance, lieu_naissance, adresse, securite_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(req, (id_artiste, nom_artiste, prenom_artiste, mail, telephone, date_de_naissance, lieu_de_naissance, adresse, securite_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction))
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('artiste', id_artiste=id_artiste))

@app.route('/artiste/<id_artiste>/supprimer')
def supprimer_artiste(id_artiste):
    """supprime l'artiste <id_artiste>"""
    mo.remove_artiste(id_artiste)
    return redirect(url_for('voir_artistes'))

# logement
@app.route('/logement/<id_logement>')
def logement(id_logement):
    """page du logement <id_logement>"""
    logement = mo.get_logement(id_logement)
    
    # Utilisez la vraie adresse du logement ici
    address = logement[1]
    coor = getCoordonnee(address)
    # Obtenez les coordonnées réelles en fonction de l'adresse
    coordinates = (coor[0], coor[2])
    
    # Vérifiez si les coordonnées sont disponibles
    if coordinates:
        lat, lng = coordinates
        c = folium.Map(location=[lat, lng], zoom_start=20)
        c.save("test.html")
    else:
        # Gérez le cas où les coordonnées ne sont pas disponibles
        c = None
    
    return render_template(
        "logement.html",
        logement=logement,
        map_path=c._repr_html_() if c else None
    )

@app.route('/ajout_logement')
def ajout_logement():
    """page d'ajout de logement"""
    return render_template(
        "ajout_logement.html"
    )

@app.route('/voir_logements')
def voir_logements():
    return render_template(
        "voir_logements.html",
        logements=mo.logements()
    )
    

@app.route('/save_logement', methods=("POST",))
def save_logement():
    """sauvegarde d'un logement"""
    nom_logement = request.form['nom_etablissement']
    adresse = request.form['adresse']
    nb_etoile = request.form['nb_etoiles']
    id_logement = mo.get_id_logement_max()+1
    
    
    mo.save_logement(id_logement, nom_logement, adresse, nb_etoile)
    
    return redirect(url_for('logement', id_logement=id_logement))

@app.route('/logement/<id_logement>/supprimer')
def supprimer_logement(id_logement):
    """supprime le logement <id_logement>"""
    mo.remove_logement(id_logement)
    return redirect(url_for('voir_logements'))

@app.route('/logement/<id_logement>/modifier')
def modifier_logement(id_logement):
    """page de l'artiste <id_logement>"""
    logement = mo.get_logement(id_logement)
    return render_template(
        "modifier_logement.html",
        logement=logement
    )

@app.route('/modif_logement/<id_logement>/<nom_etablissement>', methods=("POST",))
def confirmer_modif_logement(id_logement, nom_etablissement):
    """sauvegarde d'un logement"""
    nom = request.form['nom_etablissement']
    adresse = request.form['adresse']
    nb_etoile = request.form['nb_etoiles']
    photo = request.files['image']
    mo.confirmer_modif_logement(id_logement, nom, adresse, nb_etoile,photo)
    return redirect(url_for('logement', id_logement=id_logement))

# calendrier
@app.route('/calendrier/<jour>')
def calendrier(jour = datetime.datetime.now()):
    """page du calendrier au jour <jour>"""
    heures = HEURES_DECALAGE_1
    if type(jour) == str:
        jour = datetime.datetime.strptime(jour, "%d-%m-%Y")
    agenda = mo.concerts_agenda(heures, jour)
    lundi = (jour + datetime.timedelta(days=-(jour.weekday()+1)) + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    dimanche = (jour + datetime.timedelta(days=7-(jour.weekday()+1))).replace(hour=23, minute=59, second=59, microsecond=0)
    return render_template(
        "calendrier.html",
        concerts=mo.prochains_concerts(),
        agenda=agenda,
        heures=heures,
        date_lundi=lundi.strftime("%d-%m-%Y"),
        date_dimanche=dimanche.strftime("%d-%m-%Y")
    )

@app.route('/calendrier/redirection', methods=("POST",))
def calendrier_redirection():
    """redirige vers le calendrier du jour"""
    jour = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d")
    return redirect(url_for('calendrier', jour=jour.strftime("%d-%m-%Y")))

@app.route('/calendrier/semaine_precedente/<jour_actuel>')
def calendrier_semaine_precedente(jour_actuel = datetime.datetime.now()):
    """page du calendrier de la semaine précédent <jour_actuel>"""
    if type(jour_actuel) == str:
        jour_actuel = datetime.datetime.strptime(jour_actuel, "%d-%m-%Y")
    jour = jour_actuel + datetime.timedelta(days=-7)
    return redirect(url_for('calendrier', jour=jour.strftime("%d-%m-%Y")))

@app.route('/calendrier/semaine_suivante/<jour_actuel>')
def calendrier_semaine_suivante(jour_actuel = datetime.datetime.now()):
    """page du calendrier de la semaine suivant <jour_actuel>"""
    if type(jour_actuel) == str:
        jour_actuel = datetime.datetime.strptime(jour_actuel, "%d-%m-%Y")
    jour = jour_actuel + datetime.timedelta(days=7)
    return redirect(url_for('calendrier', jour=jour.strftime("%d-%m-%Y")))

# equipement
@app.route('/ajout_equipement')
def ajout_equipement():
    """page d'ajout d'un equipement"""
    return render_template(
        "ajout_equipement.html"
    )

@app.route('/voir_equipements')
def voir_equipements():
    """page qui affiche les equipements"""
    return render_template(
            "voir_equipements.html",
            equipements=mo.equipements()
        )

@app.route('/equipement/<id_equipement>')
def equipement(id_equipement):
    """page de l'equipement <id_equipement>"""
    equipement = mo.get_equipement(id_equipement)
    return render_template(
        "equipement.html",
        equipement=equipement
    )

@app.route('/save_equipement', methods=("POST",))
def save_equipement():
    """sauvegarde d'un equipement"""
    nom_equipement = request.form['nom_equipement']
    id_equipement = mo.get_id_equipement_max()+1
    try:
        cursor = mo.get_cursor()
        req = "INSERT INTO Equipement (id_equipement, nom_equipement) VALUES(%s, %s)"
        cursor.execute(req, (id_equipement, nom_equipement))
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('equipement', id_equipement=id_equipement))

@app.route('/equipement/<id_equipement>/supprimer')
def supprimer_equipement(id_equipement):
    """supprime l'equipement' <id_equipement>"""
    mo.remvove_equipement(id_equipement)
    return redirect(url_for('voir_equipements'))

@app.route('/equipement/<id_equipement>/modifier')
def modifier_equipement(id_equipement):
    """modifier l'equipement' <id_equipement>"""
    equipement = mo.get_equipement(id_equipement)
    return render_template(
        "modifier_equipement.html",
        equipement=equipement
    )

#type_salle
@app.route('/ajout_type_salle')
def ajout_type_salle():
    """page d'ajout d'un type de salle"""
    return render_template(
        "ajout_type_salle.html"
    )

@app.route('/save_type_salle', methods=("POST",))
def save_type_salle():
    """sauvegarde d'un type de salle"""
    nom_type_salle = request.form['nom_type_salle']
    id_type_salle = mo.get_id_type_salle_max()+1
    try:
        cursor = mo.get_cursor()
        req = "INSERT INTO Type_Salle (id_type, type_place_s) VALUES(%s, %s)"
        cursor.execute(req, (id_type_salle, nom_type_salle))
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('accueil'))

@app.route("/fiche_rider")
def afficher_rider():
    return render_template(
        "afficher_rider.html"
    )

def getCoordonnee(address):
    try:
        encoded_address = requests.utils.quote(address, safe='')

        api_url = f"https://nominatim.openstreetmap.org/search?format=json&q={encoded_address}"

        # Effectuer la requête HTTP
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifier s'il y a des erreurs HTTP

        # Analyser la réponse JSON
        # Note: Utilisez la bibliothèque json pour une meilleure gestion JSON.
        # Ici, nous utilisons simplement un affichage brut pour illustrer le concept.
        #print("Réponse du service de géocodage :")
        #print(response.text)
        #res = response.text["boundingbox"]
        response_dict = json.loads(response.text)
        for item in response_dict:
            res = item["boundingbox"]
            return res

        # Now you can access the "boundingbox" key
   

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")