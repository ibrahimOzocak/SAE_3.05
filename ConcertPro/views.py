from flask import render_template
from .app import app

@app.route('/')
def accueil():
    return render_template(
        "accueil.html"
    )

@app.route('/creer_concert')
def creer_concert():
    return render_template(
        "creer_concert.html"
    )

@app.route('/voir_prochains_concerts')
def voir_prochains_concerts():
    return render_template(
        "voir_prochains_concerts.html"
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