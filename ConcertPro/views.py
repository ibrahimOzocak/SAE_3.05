from flask import redirect, render_template, request, url_for
from .app import app
import datetime

ARTISTES = [{"nom": "Lucie"}, {"nom": "Mira"}, {"nom": "Muse"}, {"nom": "Daft Punk"}, {"nom": "Beyoncé"}, {"nom": "The Beatles"}, {"nom": "Ed Sheeran"}, {"nom": "Adele"}, {"nom": "Michael Jackson"}, {"nom": "Taylor Swift"}, {"nom": "Coldplay"}, {"nom": "Kanye West"}]
CONCERTS = [{"artiste": "Lucie", "date_debut": datetime.datetime.strptime("2023-10-26", "%Y-%m-%d"), "heure_debut":10, "salle": "Bercy", "url": "test", "nom": "yaaa", "heure_duree":2, "minute_duree":25, "jour":4}, {"artiste": "Mira", "date_debut": datetime.datetime.strptime("2023-10-24", "%Y-%m-%d"), "heure_debut":8, "salle": "Bercy", "url": "test", "nom": "test", "heure_duree":3, "minute_duree":00, "jour":1}, {"artiste": "Muse", "date_debut": datetime.datetime.strptime("2023-10-29", "%Y-%m-%d"), "heure_debut":10, "salle": "Bercy", "url": "test", "nom": "concert 1", "heure_duree":1, "minute_duree":35, "jour":6}, {"artiste": "Daft Punk", "date_debut": datetime.datetime.strptime("2023-10-23", "%Y-%m-%d"), "heure_debut":14, "salle": "Stade de France", "url": "test", "nom": "concert 2", "heure_duree":4, "minute_duree":00, "jour":1}, {"artiste": "Beyoncé", "date_debut": datetime.datetime.strptime("2023-10-24", "%Y-%m-%d"), "heure_debut":11, "salle": "Madison Square Garden", "url": "test", "nom": "concert 3", "heure_duree":1, "minute_duree":30, "jour":4}, {"artiste": "The Beatles", "date_debut": datetime.datetime.strptime("2019-04-10", "%Y-%m-%d"), "heure_debut":12, "salle": "Royal Albert Hall", "url": "test", "nom": "concert 4", "heure_duree":00, "minute_duree":45, "jour":1}, {"artiste": "Ed Sheeran", "date_debut": datetime.datetime.strptime("2019-05-05", "%Y-%m-%d"), "heure_debut":9, "salle": "Wembley Stadium", "url": "test", "nom": "concert 5", "heure_duree":3, "minute_duree":30, "jour":3}, {"artiste": "Adele", "date_debut": datetime.datetime.strptime("2019-06-12", "%Y-%m-%d"), "heure_debut":22, "salle": "The O2 Arena", "url": "test", "nom": "concert 6", "heure_duree":1, "minute_duree":25, "jour":7}, {"artiste": "Michael Jackson", "date_debut": datetime.datetime.strptime("2023-10-18", "%Y-%m-%d"), "heure_debut":8, "salle": "Tokyo Dome", "url": "test", "nom": "concert 7", "heure_duree":2, "minute_duree":00, "jour":1}, {"artiste": "Taylor Swift", "date_debut": datetime.datetime.strptime("2019-08-25", "%Y-%m-%d"), "heure_debut":15, "salle": "Arrowhead Stadium", "url": "test", "nom": "concert 8", "heure_duree":2, "minute_duree":25, "jour":3}, {"artiste": "Coldplay", "date_debut": datetime.datetime.strptime("2019-09-14", "%Y-%m-%d"), "heure_debut":11, "salle": "Estadio Wanda Metropolitano", "url": "test", "nom": "concert 9", "heure_duree":5, "minute_duree":00, "jour":5}, {"artiste": "Kanye West", "date_debut": datetime.datetime.strptime("2023-10-23", "%Y-%m-%d"), "heure_debut":13, "salle": "American Airlines Center", "url": "test", "nom": "concert 10", "heure_duree":1, "minute_duree":30, "jour":2}]
SALLES = [{"nom": "Bercy", "nbPlaces": 130, "photo":"static/images/test.png"}, {"nom": "Stade de France", "nbPlaces": 80000, "photo":"static/images/test.png"}, {"nom": "Madison Square Garden", "nbPlaces": 20000, "photo":"static/images/test.png"}, {"nom": "Royal Albert Hall", "nbPlaces": 5000, "photo":"static/images/test.png"}, {"nom": "Wembley Stadium", "nbPlaces": 90000, "photo":"static/images/test.png"}, {"nom": "The O2 Arena", "nbPlaces": 20000, "photo":"static/images/test.png"}, {"nom": "Tokyo Dome", "nbPlaces": 55000, "photo":"static/images/test.png"}, {"nom": "Arrowhead Stadium", "nbPlaces": 80000, "photo":"static/images/test.png"}, {"nom": "Estadio Wanda Metropolitano", "nbPlaces": 68000, "photo":"static/images/test.png"}, {"nom": "American Airlines Center", "nbPlaces": 21000, "photo":"static/images/test.png"}]
HEURES1 = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
PAS1 = 1
HEURES2 = [8, 10, 12, 14, 16, 18, 20, 22]
PAS2 = 2
JOUR_VOULU = datetime.datetime.now() # -datetime.timedelta(days=7) ou +datetime.timedelta(days=7) --> pour changer de semaine (- ou + 1 semaine)

@app.route('/')
def accueil():
    heures = HEURES2
    pas = PAS2
    jour = JOUR_VOULU
    agenda = concerts_agenda(CONCERTS, heures, pas)
    lundi = jour + datetime.timedelta(days=-(jour.weekday()+1)) + datetime.timedelta(days=1)
    dimanche = jour + datetime.timedelta(days=7-(jour.weekday()+1))
    return render_template(
        "accueil.html",
        agenda=agenda,
        heures=heures,
        date_lundi=lundi.strftime("%d/%m/%Y"),
        date_dimanche=dimanche.strftime("%d/%m/%Y")
    )

def concerts_agenda(liste_concerts,heures=HEURES1,pas=PAS1,jour_voulu=JOUR_VOULU):
    #initialisation de l'agenda
    agenda = {}
    for i in range(1,8):
        agenda[i] = {}
        for heure in heures:
            agenda[i][heure] = []
    #remplissage de l'agenda
    for concert in liste_concerts:
        jour = jour_voulu
        if datetime.timedelta(days=-(jour.weekday()+1))<concert["date_debut"]-jour<datetime.timedelta(days=7-(jour.weekday()+1)):
            for h in heures:
                fin_horaire = h+pas
                # format 24h obligatoire
                if fin_horaire > 23:
                    fin_horaire = datetime.time(hour=h+pas-1, minute=59)
                else:
                    fin_horaire = datetime.time(hour=h+pas)
                if not(datetime.time(hour=concert["heure_debut"]) >= fin_horaire or datetime.time(hour=concert["heure_debut"]+concert["heure_duree"],minute=concert["minute_duree"]) <= datetime.time(hour=h)):
                    agenda[concert["date_debut"].weekday()+1][h].append(concert["nom"])
    print(agenda)
    return agenda

@app.route('/creer_concert')
def creer_concert():
    return render_template(
        "creer_concert.html",
        artistes=ARTISTES,
        salles=SALLES
    )

@app.route('/voir_prochains_concerts')
def voir_prochains_concerts():
    return render_template(
        "voir_prochains_concerts.html",
        concerts=CONCERTS
    )

@app.route('/ajout_nouvelle_salle')
def ajout_nouvelle_salle():
    return render_template(
        "ajout_nouvelle_salle.html"
    )

@app.route('/voir_salles')
def voir_salles():
    return render_template(
        "voir_salles.html",
        salles = SALLES
    )

@app.route('/historique_concert')
def historique_concerts():
    return render_template(
        "historique_concerts.html",
        salles = SALLES
    )

@app.route('/save_concert', methods=("POST",))
def save_concert():
    concert = {}
    concert["artiste"] = request.form['artiste']
    concert["date_debut"] = datetime.datetime.strptime(request.form['date_debut'], "%Y-%m-%d")
    concert["salle"] = request.form['salle']
    concert["nom"] = request.form['titre']
    concert["heure_debut"] = request.form['heure_debut']
    concert["heure_duree"] = request.form['heure_duree']
    concert["minute_duree"] = request.form['minute_duree']
    concert["jour"] = 7
    CONCERTS.append(concert)
    return redirect(url_for('concert', nom=concert["nom"]))

@app.route('/concert/<nom>')
def concert(nom):
    concert = get_concert(nom)
    return render_template(
        "concert.html",
        concert=concert
    )

def get_concert(nom):
    for c in CONCERTS:
        if c["nom"] == nom:
            return c
    return None