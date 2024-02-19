from flask import redirect, render_template, request, url_for, make_response
import folium
from .app import app, db
import datetime
from . import models as mo
import requests
import json
from google.oauth2 import service_account
import googleapiclient.discovery
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from urllib.parse import unquote



HEURES_DECALAGE_1 = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23
]
HEURES_DECALAGE_2 = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]


# accueil
@app.route('/')
def accueil():
    """page d'accueil"""
    jour = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    heures = HEURES_DECALAGE_2
    lundi = (jour + datetime.timedelta(days=-(jour.weekday() + 1)) +
             datetime.timedelta(days=1)).replace(hour=0,
                                                 minute=0,
                                                 second=0,
                                                 microsecond=0)
    dimanche = (jour + datetime.timedelta(days=7 -
                                          (jour.weekday() + 1))).replace(
                                              hour=23,
                                              minute=59,
                                              second=59,
                                              microsecond=0)
    agenda = mo.concerts_agenda(heures, lundi)
    return render_template('accueil.html',
                           concerts=mo.prochains_concerts(),
                           agenda=agenda,
                           heures=heures,
                           date_lundi=lundi.strftime('%d-%m-%Y'),
                           date_dimanche=dimanche.strftime('%d-%m-%Y'))


@app.route('/plan_feu')
def plan_feu():
    """page du plan feu"""
    return render_template('plan_feu.html')


@app.route('/aide')
def aide():
    """page du plan feu"""
    return render_template('aide.html')


@app.template_filter('str')
def string_filter(value):
    return str(value)


# concert
@app.route('/creer_concert')
def creer_concert():
    """page de création de concert"""
    return render_template('creer_concert.html',
                           artistes=mo.artistes(),
                           salles=mo.salles(),
                           types=mo.type_salle(),
                           logements=mo.logements())


@app.route('/voir_prochains_concerts')
def voir_prochains_concerts():
    """page qui affiche les concerts à venir"""
    return render_template('voir_prochains_concerts.html',
                           concerts=mo.prochains_concerts(),
                           artistes=mo.artistes(),
                           salles=mo.salles())


@app.route('/historique_concert')
def historique_concerts():
    """page qui affiche les concerts passés"""
    return render_template('historique_concerts.html',
                           concerts=mo.historique_concerts(),
                           salles=mo.salles(),
                           artistes=mo.artistes())


@app.route('/save_concert', methods=('POST', ))
def save_concert():
    """sauvegarde d'un concert"""
    nom_concert = request.form['titre']
    date_debut = datetime.datetime.strptime(request.form['date_debut'],
                                            '%Y-%m-%d')
    heure_debut = datetime.datetime.strptime(request.form['heure_debut'],
                                             '%H:%M').time()
    date_heure_concert = datetime.datetime.combine(date_debut, heure_debut)
    heure_duree = datetime.datetime.strptime(request.form['duree'],
                                             '%H:%M').time().hour
    minute_duree = datetime.datetime.strptime(request.form['duree'],
                                              '%H:%M').time().minute
    duree_concert = heure_duree * 60 + minute_duree
    id_artiste = request.form['artiste']
    id_salle = request.form['salle']
    description_concert = request.form['description']
    photo = request.files['image']
    logement_artiste = request.form['logement']
    nuit = request.form['nuits']
    id = mo.get_id_concert_max() + 1

    mo.save_concert(id, nom_concert, date_heure_concert, duree_concert,
                    id_artiste, id_salle, description_concert, photo)
    mo.add_artiste_concert(id, id_artiste)
    mo.add_logement_artiste(id, id_artiste, logement_artiste, nuit)
    return redirect(url_for('concert', id=id))


@app.route('/concert/<id>')
def concert(id):
    """page pour le concert <id>"""
    le_concert = mo.get_concert(id)
    la_salle = mo.get_salle(le_concert[5])
    lartiste = mo.get_artiste(le_concert[4])
    necessaire = mo.categoriser_equipements(id, lartiste[0])
    address = la_salle[8]
    coor = getCoordonnee(address)
    c = None
    logement_artiste = mo.get_logement_artiste(le_concert[0], lartiste[0])
    if coor is not None:
        coordinates = (coor[0], coor[2])
        if coordinates:
            lat, lng = coordinates
            c = folium.Map(location=[lat, lng], zoom_start=20)
            c.save('test.html')
    return render_template('concert.html',
                           concert=le_concert,
                           salle=la_salle,
                           artiste=lartiste,
                           necessaire=necessaire,
                           logement=logement_artiste,
                           map_path=c._repr_html_() if c else None)


@app.route('/concert/<id>/supprimer')
def supprimer_concert(id):
    """supprime le concert <id>"""
    mo.remove_concert(id)
    return redirect(url_for('voir_prochains_concerts'))


@app.route('/concert/<id_concert>/modifier')
def modifier_concert(id_concert):
    """modifier le concert <id_concert>"""
    le_concert = mo.get_concert(id_concert)
    liste_salle = mo.salles()
    liste_artiste = mo.artistes()
    logements = mo.logements()
    logement_artiste = mo.get_logement_artiste(le_concert[0], le_concert[4])
    return render_template('modifier_concert.html',
                           concert=le_concert,
                           salles=liste_salle,
                           artistes=liste_artiste,
                           logements=logements,
                           logement_artiste=logement_artiste)


@app.route('/modifier_concert/<id_concert>', methods=('POST', ))
def confirmer_modif_concert(id_concert):
    """sauvegarde d'un concert"""
    nom_concert = request.form['nom_concert']
    id_artiste = request.form['artiste']
    id_salle = request.form['salle']
    date_heure_concert = request.form['date_heure_concert']
    duree_concert = request.form['duree_concert']
    description_concert = request.form['description_concert']
    photo = request.files['image']
    le_logement = request.form['logement']
    nuits = request.form['nuits']
    ancien_artiste = request.form['ancien_artiste']

    mo.confirmer_modif_concert(id_concert, nom_concert, date_heure_concert,
                               duree_concert, id_artiste, id_salle,
                               description_concert, photo)
    mo.remove_participer(id_concert, ancien_artiste)
    mo.add_artiste_concert(id_concert, id_artiste)
    mo.supprimer_logement_artiste(id_concert, ancien_artiste)
    mo.add_logement_artiste(id_concert, id_artiste, le_logement, nuits)

    return redirect(url_for('concert', id=id_concert))


# salle
@app.route('/ajout_nouvelle_salle')
def ajout_nouvelle_salle():
    """page de création de salle"""
    return render_template('ajout_nouvelle_salle.html',
                           types=mo.get_type_salles())


@app.route('/salle/<id>')
def salle(id):
    """page de salle <id>"""
    la_salle = mo.get_salle(id)
    lequipement = mo.get_equipement_salle(id)
    type_salle = mo.get_type_salle(id)

    # Utilisez la vraie adresse du salle ici
    address = la_salle[8]
    coor = getCoordonnee(address)
    # Gérez le cas où les coordonnées ne sont pas disponibles
    c = None
    if coor is not None:
        # Obtenez les coordonnées réelles en fonction de l'adresse
        coordinates = (coor[0], coor[2])
        # Vérifiez si les coordonnées sont disponibles
        if coordinates:
            lat, lng = coordinates
            c = folium.Map(location=[lat, lng], zoom_start=20)
            c.save('test.html')
    return render_template('salle.html',
                           salle=la_salle,
                           equipement=lequipement,
                           type_salle=type_salle,
                           map_path=c._repr_html_() if c else None)


@app.route('/voir_salles')
def voir_salles():
    """page qui affiche les salles"""
    return render_template('voir_salles.html', salles=mo.salles())


@app.route('/save_salle', methods=('POST', ))
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
    adresse_salle = adresse_salle + ', ' + code_postal_salle
    loge = 'non'
    acces_pmr = 'non'
    for elem in request.form:
        if elem == 'loge':
            loge = 'oui'
        elif elem == 'accueilpmr':
            acces_pmr = 'oui'
    id = mo.get_id_salle_max() + 1
    mo.save_salle(id, nom_salle, nb_places, profondeur_scene, longueur_scene,
                  telephone_salle, type_place, description_salle, photo,
                  adresse_salle, loge, acces_pmr)

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
    return render_template('ajout_artiste.html', styles=mo.styles_musisque())


@app.route('/voir_artistes')
def voir_artistes():
    """page voir les artistes"""
    return render_template('voir_artistes.html', artistes=mo.artistes())


@app.route('/artiste/<id_artiste>')
def artiste(id_artiste):
    """page de l'artiste <id_artiste>"""
    lartiste = mo.get_artiste(id_artiste)
    concerts = mo.get_concerts_artiste(id_artiste)
    return render_template('artiste.html', artiste=lartiste, concerts=concerts)


@app.route('/confirmer_artiste/<id_artiste>', methods=('POST', ))
def confirmer_modif_artiste(id_artiste):
    """sauvegarde d'un artiste"""
    prenom_artiste = request.form['prenom']
    nom_artiste = request.form['nom']
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
    genre_musical = request.form['genre']
    photo = request.files['image']
    mo.confirmer_modif_artiste(id_artiste, prenom_artiste, nom_artiste,
                               nom_de_scene, mail, telephone,
                               date_de_naissance, lieu_de_naissance, adresse,
                               numero_secu_sociale, cni, date_delivrance_cni,
                               date_expiration_cni, carte_reduction,
                               genre_musical, photo)
    return redirect(url_for('artiste', id_artiste=id_artiste))


@app.route('/confirmer_salle/<id_salle>', methods=('POST', ))
def confirmer_modif_salle(id_salle):
    """sauvegarde d'un artiste"""
    nom = request.form['nom']
    description = request.form['description']
    loge = request.form['loge']
    nombre_place = request.form['nombre de places']
    adresse = request.form['adresse']
    telephone = request.form['telephone']
    profondeur_scene = request.form['profondeur scene']
    longueur_scene = request.form['longueur scene']
    photo = request.files['image']
    type_place = request.form['type']
    mo.confirmer_modif_salle(id_salle, nom, description, loge, nombre_place,
                             adresse, telephone, profondeur_scene,
                             longueur_scene, photo, type_place)
    return redirect(url_for('salle', id=id_salle))


@app.route('/artiste/<id_artiste>/modifier')
def modifier_artiste(id_artiste):
    """page de l'artiste <id_artiste>"""
    lartiste = mo.get_artiste(id_artiste)
    styles = mo.styles_musisque()
    return render_template('modifier_artiste.html',
                           artiste=lartiste,
                           styles=styles)


@app.route('/salle/<id_salle>/modifier')
def modifier_salle(id_salle):
    """page de la salle <id_salle>"""
    la_salle = mo.get_salle(id_salle)
    type_salle = mo.get_type_salle(id_salle)
    types = mo.get_type_salles()
    return render_template('modifier_salle.html',
                           salle=la_salle,
                           type_salle=type_salle,
                           types=types)


@app.route('/save_artiste', methods=('POST', ))
def save_artiste():
    """sauvegarde d'un artiste"""
    nom_artiste = request.form['nom']
    prenom_artiste = request.form['prenom']
    nom_scene = request.form['nom_scene']
    mail = request.form['mail']
    telephone = request.form['telephone']
    date_de_naissance = datetime.datetime.strptime(
        request.form['date_naissance'], '%Y-%m-%d')
    lieu_de_naissance = request.form['lieu_naissance']
    adresse = request.form['adresse']
    securite_sociale = request.form['num_secu_sociale']
    cni = request.form['cni']
    date_delivrance_cni = datetime.datetime.strptime(
        request.form['date_delivrance'], '%Y-%m-%d')
    date_expiration_cni = datetime.datetime.strptime(
        request.form['date_expiration'], '%Y-%m-%d')
    carte_reduction = request.form['carte_train']
    genre_musical = request.form['genre']
    id_artiste = mo.get_id_artiste_max() + 1
    mo.save_artiste(id_artiste, nom_artiste, prenom_artiste, mail, telephone,
                    date_de_naissance, lieu_de_naissance, adresse,
                    securite_sociale, cni, date_delivrance_cni,
                    date_expiration_cni, carte_reduction, genre_musical,
                    nom_scene)
    return redirect(url_for('artiste', id_artiste=id_artiste))


@app.route('/save_artiste_to_rider')
def save_artiste_to_rider():
    """sauvegarde d'un artiste"""
    informations = request.args.get('informations')
    informations = unquote(informations).split(',')
    chemin_fichier = './ConcertPro/static/json/rider.json'
    id_artiste = mo.get_id_artiste_max() + 1

    try:
        with open(chemin_fichier, 'r') as fichier:
            data = json.load(fichier)
        for d in data:
            if informations[-1] == d[0] or id_artiste == d[1]:
                return redirect(url_for('creer_concert'))
        data.append((informations[-1], id_artiste))
        with open(chemin_fichier, 'w') as fichier:
            json.dump(data, fichier, indent=2)
    except:
        pass

    mo.save_artiste(id_artiste, informations[2], informations[3],
                    informations[20], informations[21], informations[4],
                    informations[5], informations[6], informations[7],
                    informations[9], informations[10], informations[11],
                    informations[12], informations[-2], informations[22],
                    informations[8])

    return redirect(url_for('creer_concert'))


@app.route('/artiste/<id_artiste>/supprimer')
def supprimer_artiste(id_artiste):
    """supprime l'artiste <id_artiste>"""
    mo.remove_artiste(id_artiste)
    return redirect(url_for('voir_artistes'))


@app.route('/fiche_rider/modifier_rider')
def modifier_rider():
    """modifier le rider"""
    informations = request.args.get('informations')
    informations = unquote(informations).split(',')
    base = request.args.get('base')
    base = unquote(base).split(',')
    if '/' in informations[4]:
        informations[4] = convert_date_format(informations[4])
    if '/' in informations[10]:
        informations[10] = convert_date_format(informations[10])
    if '/' in informations[11]:
        informations[11] = convert_date_format(informations[11])
    return render_template('modifier_rider.html', b=base, info=informations)

def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    nouvelle_date_str = date_obj.strftime('%Y-%m-%d')
    return nouvelle_date_str


# logement
@app.route('/logement/<id_logement>')
def logement(id_logement):
    """page du logement <id_logement>"""
    logement = mo.get_logement(id_logement)
    # Utilisez la vraie adresse du logement ici
    address = logement[1]
    coor = getCoordonnee(address)
    # Obtenez les coordonnées réelles en fonction de l'adresse
    c = None
    if coor is not None:
        coordinates = (coor[0], coor[2])
        # Vérifiez si les coordonnées sont disponibles
        if coordinates:
            lat, lng = coordinates
            c = folium.Map(location=[lat, lng], zoom_start=20)
            c.save('test.html')
    return render_template('logement.html',
                           logement=logement,
                           map_path=c._repr_html_() if c else None)


@app.route('/ajout_logement')
def ajout_logement():
    """page d'ajout de logement"""
    return render_template('ajout_logement.html')


@app.route('/voir_logements')
def voir_logements():
    return render_template('voir_logements.html', logements=mo.logements())


@app.route('/save_logement', methods=('POST', ))
def save_logement():
    """sauvegarde d'un logement"""
    nom_logement = request.form['nom_etablissement']
    adresse = request.form['adresse']
    nb_etoile = request.form['nb_etoiles']
    id_logement = mo.get_id_logement_max() + 1
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
    le_logement = mo.get_logement(id_logement)
    return render_template('modifier_logement.html', logement=le_logement)


@app.route('/modif_logement/<id_logement>', methods=('POST', ))
def confirmer_modif_logement(id_logement):
    """sauvegarde d'un logement"""
    nom = request.form['nom_etablissement']
    adresse = request.form['adresse']
    nb_etoile = request.form['nb_etoiles']
    mo.confirmer_modif_logement(id_logement, nom, adresse, nb_etoile)
    return redirect(url_for('logement', id_logement=id_logement))


# calendrier
@app.route('/calendrier/<jour>')
def calendrier(jour=datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)):
    """page du calendrier au jour <jour>"""
    heures = HEURES_DECALAGE_1
    if type(jour) == str:
        jour = datetime.datetime.strptime(jour, '%d-%m-%Y')
    agenda = mo.concerts_agenda(heures, jour)
    lundi = (jour + datetime.timedelta(days=-(jour.weekday() + 1)) +
             datetime.timedelta(days=1)).replace(hour=0,
                                                 minute=0,
                                                 second=0,
                                                 microsecond=0)
    dimanche = (jour + datetime.timedelta(days=7 -
                                          (jour.weekday() + 1))).replace(
                                              hour=23,
                                              minute=59,
                                              second=59,
                                              microsecond=0)
    return render_template('calendrier.html',
                           concerts=mo.prochains_concerts(),
                           agenda=agenda,
                           heures=heures,
                           date_lundi=lundi.strftime('%d-%m-%Y'),
                           date_dimanche=dimanche.strftime('%d-%m-%Y'))


@app.route('/calendrier/redirection', methods=('POST', ))
def calendrier_redirection():
    """redirige vers le calendrier du jour"""
    jour = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
    return redirect(url_for('calendrier', jour=jour.strftime('%d-%m-%Y')))


@app.route('/calendrier/semaine_precedente/<jour_actuel>')
def calendrier_semaine_precedente(jour_actuel=datetime.datetime.now()):
    """page du calendrier de la semaine précédent <jour_actuel>"""
    if type(jour_actuel) == str:
        jour_actuel = datetime.datetime.strptime(jour_actuel, '%d-%m-%Y')
    jour = jour_actuel + datetime.timedelta(days=-7)
    return redirect(url_for('calendrier', jour=jour.strftime('%d-%m-%Y')))


@app.route('/calendrier/semaine_suivante/<jour_actuel>')
def calendrier_semaine_suivante(jour_actuel=datetime.datetime.now()):
    """page du calendrier de la semaine suivant <jour_actuel>"""
    if type(jour_actuel) == str:
        jour_actuel = datetime.datetime.strptime(jour_actuel, '%d-%m-%Y')
    jour = jour_actuel + datetime.timedelta(days=7)
    return redirect(url_for('calendrier', jour=jour.strftime('%d-%m-%Y')))


# equipement
@app.route('/ajout_equipement')
def ajout_equipement():
    """page d'ajout d'un equipement"""
    return render_template('ajout_equipement.html')


@app.route('/ajout_equipement_concert/<id_concert>')
def ajout_equipement_concert(id_concert):
    """page d'ajout d'un equipement au concert <id_concert>"""
    return render_template('ajout_equipement_concert.html',
                           id_concert=id_concert,
                           equipements=mo.get_equipements_concert(id_concert))


@app.route('/ajout_necessaire_concert/<id_concert>')
def ajout_necessaire_concert(id_concert):
    """page d'ajout d'un equipement nécessaire au concert <id_concert>"""
    return render_template(
        'ajout_necessaire_concert.html',
        id_concert=id_concert,
        equipements=mo.get_tous_equipements_concert(id_concert))


@app.route('/ajout_equipement_salle/<id_salle>')
def ajout_equipement_salle(id_salle):
    """page d'ajout d'un equipement à la salle <id_salle>"""
    return render_template('ajout_equipement_salle.html',
                           id_salle=id_salle,
                           equipements=mo.get_tous_equipements_salle(id_salle))


@app.route('/voir_equipements')
def voir_equipements():
    """page qui affiche les equipements"""
    return render_template('voir_equipements.html',
                           equipements=mo.equipements())


@app.route('/equipement/<id_equipement>')
def equipement(id_equipement):
    """page de l'equipement <id_equipement>"""
    lequipement = mo.get_equipement(id_equipement)
    return render_template('equipement.html', equipement=lequipement)


@app.route('/save_equipement', methods=('POST', ))
def save_equipement():
    """sauvegarde d'un equipement"""
    nom_equipement = request.form['nom_equipement']
    id_equipement = mo.get_id_equipement_max() + 1
    try:
        cursor = mo.get_cursor()
        req = 'INSERT INTO Equipement (id_equipement, nom_equipement) VALUES(%s, %s)'
        cursor.execute(req, (id_equipement, nom_equipement))
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('equipement', id_equipement=id_equipement))


@app.route('/save_equipement_concert/<id_concert>', methods=('POST', ))
def save_equipements_concert(id_concert):
    """sauvegarde d'un equipement pour le concert <id_concert>"""
    for elem in request.form:
        if elem.isnumeric():
            quantite = request.form[elem]
            elem = int(elem)
            mo.save_equipement_concert(id_concert, elem, quantite)
    return redirect(url_for('concert', id=id_concert))


@app.route('/save_necessaire_concert/<id_concert>', methods=('POST', ))
def save_necessaire_concert(id_concert):
    """sauvegarde d'un equipement pour le concert <id_concert>"""
    for elem in request.form:
        if elem.isnumeric():
            quantite = int(request.form[elem])
            if 'hidden' + elem in request.form:
                hidden = int(request.form.get('hidden' + elem))
            else:
                hidden = 0
            elem = int(elem)
            id_artiste = mo.get_concert(id_concert)[4]
            mo.save_necessaire_concert(id_concert, elem, quantite, id_artiste,
                                       hidden)
    return redirect(url_for('concert', id=id_concert))


@app.route('/save_equipement_salle/<id_salle>', methods=('POST', ))
def save_equipements_salle(id_salle):
    """sauvegarde d'un equipement pour la salle <id_salle>"""
    for elem in request.form:
        if elem.isnumeric():
            quantite = int(request.form[elem])
            if 'hidden' + elem in request.form:
                hidden = int(request.form.get('hidden' + elem))
            else:
                hidden = 0
            elem = int(elem)
            mo.save_equipement_salle(id_salle, elem, quantite, hidden)
    return redirect(url_for('salle', id=id_salle))


@app.route('/equipement/<id_equipement>/supprimer')
def supprimer_equipement(id_equipement):
    """supprime l'equipement' <id_equipement>"""
    mo.remvove_equipement(id_equipement)
    return redirect(url_for('voir_equipements'))


@app.route('/equipement/<id_equipement>/modifier')
def modifier_equipement(id_equipement):
    """modifier l'equipement' <id_equipement>"""
    lequipement = mo.get_equipement(id_equipement)
    return render_template('modifier_equipement.html', equipement=lequipement)


@app.route('/confirmer_equipement/<id_equipement>', methods=('POST', ))
def confirmer_modif_equipement(id_equipement):
    """sauvegarde d'un equipement"""
    nom = request.form['equipement']
    mo.confirmer_modif_equipement(id_equipement, nom)
    return redirect(url_for('equipement', id_equipement=id_equipement))


#type_salle
@app.route('/ajout_type_salle')
def ajout_type_salle():
    """page d'ajout d'un type de salle"""
    return render_template('ajout_type_salle.html')


@app.route('/save_type_salle', methods=('POST', ))
def save_type_salle():
    """sauvegarde d'un type de salle"""
    nom_type_salle = request.form['nom_type_salle']
    id_type_salle = mo.get_id_type_salle_max() + 1
    try:
        cursor = mo.get_cursor()
        req = 'INSERT INTO Type_Salle (id_type, type_place_s) VALUES(%s, %s)'
        cursor.execute(req, (id_type_salle, nom_type_salle))
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('accueil'))


def generate_pdf_file(file_path, title, content):
    # Créer le fichier PDF
    pdf = canvas.Canvas(file_path, pagesize=letter)
    # Calculer la position horizontale pour centrer le texte
    width = letter
    title_width = pdf.stringWidth(title, 'Helvetica-Bold', 16)
    title_x = (width - title_width) / 2
    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(title_x, 750, title)
    pdf.setFont('Helvetica', 12)
    pdf.drawString(30, 730, 'Ce rider fait partie intégrante du contrat.')
    pdf.drawString(30, 710,
                   'Merci de le respecter et de le prendre en considération.')
    pdf.drawString(
        30, 690,
        'Afin que tout le monde passe une bonne journée et gagne du temps, lisez-le attentivement'
    )
    pdf.drawString(
        30, 670,
        'et communiquez-nous par avance toute objection, question ou impossibilité relative à nos demandes.'
    )
    pdf.drawString(
        30, 650,
        'Toute modification devra faire l’objet d’un accord préalable des deux parties.'
    )
    pdf.drawString(30, 630, 'Merci d’avance.')
    ind = 0
    for c in content:
        pdf.setFont(c.split(':')[0], 12)
        title_width = pdf.stringWidth(c.split(':')[1], c.split(':')[0], 12)
        title_x = (width - title_width) / 2
        if 610 - ind * 40 <= 0:
            ind = 0
            pdf.showPage()
        pdf.drawString(title_x, 610 - ind * 40, c.split(':')[1])
        ind += 1
    pdf.save()
    return pdf


@app.route('/fiche_rider')
def afficher_rider():
    credentials = service_account.Credentials.from_service_account_file(
        './concertpro-89fff3dd57e8.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    service = googleapiclient.discovery.build('sheets',
                                              'v4',
                                              credentials=credentials)
    spreadsheet_id = '1kpj-WOIBMWlcQ0UjUBzClUZHpHbAcNtbs1boWUaYemM'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range='reponse_formulaire').execute()
    values = result.get('values', [])    
    return render_template('afficher_rider.html',
                           values=values)


@app.route('/fiche_rider/rider')
def rider():
    informations = request.args.get('informations')
    informations = unquote(informations).split(',')
    html_content = render_template('rider.html', informations=informations)
    css_path = './ConcertPro/static/css/rider.css'
    from weasyprint import HTML, CSS
    pdf = HTML(string=html_content).write_pdf(
        stylesheets=[CSS(filename=css_path)])
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers[
        'Content-Disposition'] = 'attachment; filename=fiche_rider.pdf'
    return response


@app.route('/fiche_rider/fiche_rider')
def fiche_rider():
    informations = request.args.get('informations')
    informations = unquote(informations).split(',')
    base = request.args.get('base')
    base = unquote(base).split(',')
    return render_template('fiche_rider.html', b=base, info=informations)


def getCoordonnee(address):
    try:
        encoded_address = requests.utils.quote(address, safe='')
        api_url = f'https://nominatim.openstreetmap.org/search?format=json&q={encoded_address}'
        # Effectuer la requête HTTP
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifier s'il y a des erreurs HTTP
        response_dict = json.loads(response.text)
        for item in response_dict:
            res = item['boundingbox']
            return res
    except requests.exceptions.RequestException as e:
        print(f'Erreur lors de la requête HTTP : {e}')


# Gestion des erreurs
@app.errorhandler(404)
def not_found_error(error):
    print(error)
    return render_template('erreur.html',
                           num_erreur=404,
                           message='Page non trouvée'), 404


@app.errorhandler(500)
def not_found_error(error):
    print(error)
    return render_template('erreur.html',
                           num_erreur=500,
                           message='Erreur interne du serveur'), 500
