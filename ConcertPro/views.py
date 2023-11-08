import random
from flask import redirect, render_template, request, url_for
from .app import app, db
import datetime
from . import models as mo

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
    id_artiste = mo.get_artiste(request.form['artiste'])[0]
    id_salle = mo.get_salle(request.form['salle'])[0]
    description_concert = request.form['description']
    photo = "test.png"
    try:
        cursor = mo.get_cursor()
        req = "INSERT INTO Concert (id_concert, nom_concert, date_heure_concert, duree_concert, id_artiste, id_salle, description_concert, photo) VALUES("+str(mo.get_id_concert_max()+1)+", '" + str(nom_concert) + "', '" + str(date_heure_concert) + "', " + str(duree_concert) + ", " + str(id_artiste) + ", " + str(id_salle) + ", '" + str(description_concert) + "', '" + str(photo) + "')"
        cursor.execute(req)
        mo.db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('concert', nom=nom_concert))

@app.route('/concert/<nom>')
def concert(nom):
    """page pour le concert <nom>"""
    concert = mo.get_concert(nom)
    return render_template(
        "concert.html",
        concert=concert
    )

@app.route('/concert/<nom>/supprimer')
def supprimer_concert(nom):
    """supprime le concert <nom>"""
    mo.remove_concert(nom)
    return redirect(url_for('accueil'))

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

@app.route('/salle/<nom>')
def salle(nom):
    """page pour la salle <nom>"""
    salle = mo.get_salle(nom)
    return render_template(
        "salle.html",
        salle=salle
    )

@app.route('/save_salle', methods=("POST",))
def save_salle():
    """sauvegarde d'une salle"""
    nom_salle = request.form['titre']
    nb_places = request.form['place']
    profondeur_scene = request.form['profondeur']
    longueur_scene = request.form['longueur']
    description_salle = request.form['description']
    adresse_salle = request.form['adresse']
    telephone_salle = request.form['telephone']
    code_postal_salle = request.form['postalville']
    type_place = request.form['typeplace']
    photo = "test.png"
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
    try:
        cursor = mo.get_cursor()
        req = "INSERT INTO Salle (id_salle, id_type_salle, loge, nom_salle, nb_places, profondeur_scene, longueur_scene, description_salle,adresse_salle,telephone_salle, accueil_pmr) VALUES("+str(mo.get_id_salle_max()+1) + "," + str(mo.get_id_type_salles(type_place)) + ", '" + str(loge) + "', '" + str(nom_salle) + "', " + str(nb_places) + ", " + str(profondeur_scene) + ", " + str(longueur_scene) + ", '" + str(description_salle) + "', '" + str(adresse_salle) + "', '" + str(telephone_salle) +  "', '" + str(acces_pmr) + "')"
        cursor.execute(req)
        mo.db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('salle', nom=nom_salle))

@app.route('/salle/<nom>/supprimer')
def supprimer_salle(nom):
    """supprime la salle <nom>"""
    mo.remove_salle(nom)
    return redirect(url_for('accueil'))

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
    

@app.route('/artiste/<nom_artiste>')
def artiste(nom_artiste):
    """page de l'artiste <nom_artiste>"""
    artiste = mo.get_artiste(nom_artiste)
    return render_template(
        "artiste.html",
        artiste=artiste
    )

@app.route('/traiter_formulaire/<id_artiste>/<nom_artiste>', methods=("POST",))
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
    
    mo.confirmer_modif_artiste(id_artiste, nom_artiste, nom_de_scene, mail, telephone, date_de_naissance, lieu_de_naissance,
        adresse, numero_secu_sociale, cni, date_delivrance_cni, date_expiration_cni, carte_reduction)
    
    return redirect(url_for('artiste', nom_artiste=nom_artiste))

@app.route('/traiter_formulaire/<id_salle>/<nom_salle>', methods=("POST",))
def confirmer_modif_salle(id_salle, nom_salle):
    """sauvegarde d'un artiste"""
    
    description = request.form['description_salle']
    loge = request.form['loge']
    nombre_place = request.form['nb_places']
    adresse = request.form['adresse_salle']
    telephone = request.form['telephone_salle']
    profondeur_scene = request.form['profondeur_scene']
    longueur_scene = request.form['longueur_scene']
    
    mo.confirmer_modif_artiste(id_salle, nom_salle, description, loge, nombre_place, adresse, telephone,
        profondeur_scene, longueur_scene)
    
    return redirect(url_for('salle', nom_salle=nom_salle))
    
@app.route('/artiste/<nom_artiste>/modifier')
def modifier_artiste(nom_artiste):
    """page de l'artiste <nom_artiste>"""
    artiste = mo.get_artiste(nom_artiste)
    return render_template(
        "modifier_artiste.html",
        artiste=artiste
    )

@app.route('/salle/<nom_salle>/modifier')
def modifier_salle(nom_salle):
    """page de la salle <nom_salle>"""
    salle = mo.get_salle(nom_salle)
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
    try:
        cursor = mo.get_cursor()
        req = "INSERT INTO Artiste (id_artiste, nom_artiste, prenom_artiste, mail, telephone, date_de_naissance, lieu_naissance, adresse, securite_social, cni, date_delivrance_cni, date_expiration_cni, carte_reduction) VALUES("+str(mo.get_id_artiste_max()+1)+", '" + str(nom_artiste) + "', '" + str(prenom_artiste) + "', '" + str(mail) + "', '" + str(telephone) + "', '" + str(date_de_naissance) + "', '" + str(lieu_de_naissance) + "', '" + str(adresse) + "', '" + str(securite_sociale) + "', '" + str(cni) + "', '" + str(date_delivrance_cni) + "', '" + str(date_expiration_cni) + "', '" + str(carte_reduction) + "')"
        cursor.execute(req)
        db.commit()
        mo.close_cursor(cursor)
    except Exception as e:
        print(e.args)
    return redirect(url_for('artiste', nom_artiste=nom_artiste))

@app.route('/artiste/<nom_artiste>/supprimer')
def supprimer_artiste(nom_artiste):
    """supprime l'artiste <nom_artiste>"""
    mo.remove_artiste(nom_artiste)
    return redirect(url_for('accueil'))

# logement
@app.route('/logement/<nom_etablissement>')
def logement(nom_etablissement):
    """page du logement <nom_etablissement>"""
    logement = mo.get_logement(nom_etablissement)
    return render_template(
        "logement.html",
        logement=logement
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
    logement = {}
    logement["nom_etablissement"] = request.form['Entrer_nometablissement']
    logement["adresse_ville_codepostal"] = request.form['Entrer_adresse']
    logement["nb_etoile"] = request.form['Entrer_nbetoiles']
    return redirect(url_for('logement', nom_etablissement=logement["nom_etablissement"]))

@app.route('/logement/<nom_etablissement>/supprimer')
def supprimer_logement(nom_etablissement):
    """supprime le logement >nom_etablissement>"""
    mo.remove_logement(nom_etablissement)
    return redirect(url_for('accueil'))

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

@app.route('/logement/<nom_etablissement>/modifier')
def modifier_logement(nom_etablissement):
    """page de l'artiste <nom_etablissement>"""
    logement = mo.get_logement(nom_etablissement)
    return render_template(
        "modifier_logement.html",
        logement=logement
    )

@app.route('/traiter_formulaire/<id_logement>/<nom_etablissement>', methods=("POST",))
def confirmer_modif_logement(id_logement, nom_etablissement):
    """sauvegarde d'un logement"""
    
    
    adresse = request.form['adresse_ville_codepostal']
    nb_etoile = request.form['nb_etoile']
    
    mo.confirmer_modif_artiste(id_logement, nom_etablissement,adresse, nb_etoile)
    
    return redirect(url_for('logement', nom_etablissement=nom_etablissement))