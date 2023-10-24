from flask import render_template
from .app import app

ARTISTES = [{"nom": "Lucie"}, {"nom": "Mira"}, {"nom": "Muse"}, {"nom": "Daft Punk"}, {"nom": "Beyoncé"}, {"nom": "The Beatles"}, {"nom": "Ed Sheeran"}, {"nom": "Adele"}, {"nom": "Michael Jackson"}, {"nom": "Taylor Swift"}, {"nom": "Coldplay"}, {"nom": "Kanye West"}]
CONCERTS = [{"artiste": "Lucie", "date_debut": "2023-10-24", "date_fin": "2023-10-24", "salle": "Bercy", "url": "test", "nom": "yaaa", "heure_debut":20, "heure_fin":21, "jour":4}, {"artiste": "Mira", "date_debut": "2023-10-24", "date_fin": "2023-10-24", "salle": "Bercy", "url": "test", "nom": "test", "heure_debut":8, "heure_fin":12, "jour":1}, {"artiste": "Muse", "date_debut": "2019-08:00", "date_fin": "2019:10:00", "salle": "Bercy", "url": "test", "nom": "concert 1", "heure_debut":8, "heure_fin":12, "jour":6}, {"artiste": "Daft Punk", "date_debut": "2019-02-15", "date_fin": "2019-02-15", "salle": "Stade de France", "url": "test", "nom": "concert 2", "heure_debut":8, "heure_fin":12, "jour":1}, {"artiste": "Beyoncé", "date_debut": "2019-03-20", "date_fin": "2019-03-20", "salle": "Madison Square Garden", "url": "test", "nom": "concert 3", "heure_debut":8, "heure_fin":12, "jour":4}, {"artiste": "The Beatles", "date_debut": "2019-04-10", "date_fin": "2019-04-10", "salle": "Royal Albert Hall", "url": "test", "nom": "concert 4", "heure_debut":8, "heure_fin":12, "jour":1}, {"artiste": "Ed Sheeran", "date_debut": "2019-05-05", "date_fin": "2019-05-05", "salle": "Wembley Stadium", "url": "test", "nom": "concert 5", "heure_debut":8, "heure_fin":12, "jour":3}, {"artiste": "Adele", "date_debut": "2019-06-12", "date_fin": "2019-06-12", "salle": "The O2 Arena", "url": "test", "nom": "concert 6", "heure_debut":8, "heure_fin":12, "jour":7}, {"artiste": "Michael Jackson", "date_debut": "2019-07-08", "date_fin": "2019-07-08", "salle": "Tokyo Dome", "url": "test", "nom": "concert 7", "heure_debut":8, "heure_fin":12, "jour":1}, {"artiste": "Taylor Swift", "date_debut": "2019-08-25", "date_fin": "2019-08-25", "salle": "Arrowhead Stadium", "url": "test", "nom": "concert 8", "heure_debut":8, "heure_fin":12, "jour":3}, {"artiste": "Coldplay", "date_debut": "2019-09-14", "date_fin": "2019-09-14", "salle": "Estadio Wanda Metropolitano", "url": "test", "nom": "concert 9", "heure_debut":8, "heure_fin":12, "jour":5}, {"artiste": "Kanye West", "date_debut": "2019-10-03", "date_fin": "2019-10-03", "salle": "American Airlines Center", "url": "test", "nom": "concert 10", "heure_debut":8, "heure_fin":12, "jour":2}]
SALLES = [{"nom": "Bercy", "nbPlaces": 130}, {"nom": "Stade de France", "nbPlaces": 80000}, {"nom": "Madison Square Garden", "nbPlaces": 20000}, {"nom": "Royal Albert Hall", "nbPlaces": 5000}, {"nom": "Wembley Stadium", "nbPlaces": 90000}, {"nom": "The O2 Arena", "nbPlaces": 20000}, {"nom": "Tokyo Dome", "nbPlaces": 55000}, {"nom": "Arrowhead Stadium", "nbPlaces": 80000}, {"nom": "Estadio Wanda Metropolitano", "nbPlaces": 68000}, {"nom": "American Airlines Center", "nbPlaces": 21000}]
HEURES1 = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
PAS1 = 1
HEURES2 = [8, 10, 12, 14, 16, 18, 20, 22]
PAS2 = 2

@app.route('/')
def accueil():
    return render_template(
        "accueil.html",
        concerts=CONCERTS,
        heures=HEURES2,
        pas=PAS2
    )

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
        "voir_salles.html"
    )

@app.route('/historique_concert')
def historique_concerts():
    return render_template(
        "historique_concerts.html"
    )