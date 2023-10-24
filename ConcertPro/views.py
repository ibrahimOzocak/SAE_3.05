from flask import redirect, render_template, request, url_for
from .app import app

ARTISTES = [{"nom": "Lucie"}, {"nom": "Mira"}, {"nom": "Muse"}, {"nom": "Daft Punk"}, {"nom": "Beyoncé"}, {"nom": "The Beatles"}, {"nom": "Ed Sheeran"}, {"nom": "Adele"}, {"nom": "Michael Jackson"}, {"nom": "Taylor Swift"}, {"nom": "Coldplay"}, {"nom": "Kanye West"}]
CONCERTS = [{"artiste": "Lucie", "date_debut": "2023-10-24", "heure_debut":8, "salle": "Bercy", "url": "test", "nom": "yaaa", "heure_duree":20, "minute_duree":25, "jour":4}, {"artiste": "Mira", "date_debut": "2023-10-24", "heure_debut":8, "salle": "Bercy", "url": "test", "nom": "test", "heure_duree":8, "minute_duree":25, "jour":1}, {"artiste": "Muse", "date_debut": "2019-08:00", "heure_debut":8, "salle": "Bercy", "url": "test", "nom": "concert 1", "heure_duree":8, "minute_duree":25, "jour":6}, {"artiste": "Daft Punk", "date_debut": "2019-02-15", "heure_debut":8, "salle": "Stade de France", "url": "test", "nom": "concert 2", "heure_duree":8, "minute_duree":25, "jour":1}, {"artiste": "Beyoncé", "date_debut": "2019-03-20", "heure_debut":8, "salle": "Madison Square Garden", "url": "test", "nom": "concert 3", "heure_duree":8, "minute_duree":25, "jour":4}, {"artiste": "The Beatles", "date_debut": "2019-04-10", "heure_debut":8, "salle": "Royal Albert Hall", "url": "test", "nom": "concert 4", "heure_duree":8, "minute_duree":25, "jour":1}, {"artiste": "Ed Sheeran", "date_debut": "2019-05-05", "heure_debut":8, "salle": "Wembley Stadium", "url": "test", "nom": "concert 5", "heure_duree":8, "minute_duree":25, "jour":3}, {"artiste": "Adele", "date_debut": "2019-06-12", "heure_debut":8, "salle": "The O2 Arena", "url": "test", "nom": "concert 6", "heure_duree":8, "minute_duree":25, "jour":7}, {"artiste": "Michael Jackson", "date_debut": "2019-07-08", "heure_debut":8, "salle": "Tokyo Dome", "url": "test", "nom": "concert 7", "heure_duree":8, "minute_duree":25, "jour":1}, {"artiste": "Taylor Swift", "date_debut": "2019-08-25", "heure_debut":8, "salle": "Arrowhead Stadium", "url": "test", "nom": "concert 8", "heure_duree":8, "minute_duree":25, "jour":3}, {"artiste": "Coldplay", "date_debut": "2019-09-14", "heure_debut":8, "salle": "Estadio Wanda Metropolitano", "url": "test", "nom": "concert 9", "heure_duree":8, "minute_duree":25, "jour":5}, {"artiste": "Kanye West", "date_debut": "2019-10-03", "heure_debut":8, "salle": "American Airlines Center", "url": "test", "nom": "concert 10", "heure_duree":8, "minute_duree":25, "jour":2}]
SALLES = [{"nom": "Bercy", "nbPlaces": 130, "photo":"static/images/test.png"}, {"nom": "Stade de France", "nbPlaces": 80000, "photo":"static/images/test.png"}, {"nom": "Madison Square Garden", "nbPlaces": 20000, "photo":"static/images/test.png"}, {"nom": "Royal Albert Hall", "nbPlaces": 5000, "photo":"static/images/test.png"}, {"nom": "Wembley Stadium", "nbPlaces": 90000, "photo":"static/images/test.png"}, {"nom": "The O2 Arena", "nbPlaces": 20000, "photo":"static/images/test.png"}, {"nom": "Tokyo Dome", "nbPlaces": 55000, "photo":"static/images/test.png"}, {"nom": "Arrowhead Stadium", "nbPlaces": 80000, "photo":"static/images/test.png"}, {"nom": "Estadio Wanda Metropolitano", "nbPlaces": 68000, "photo":"static/images/test.png"}, {"nom": "American Airlines Center", "nbPlaces": 21000, "photo":"static/images/test.png"}]
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
    concert["date_debut"] = request.form['date_debut']
    concert["salle"] = request.form['salle']
    concert["nom"] = request.form['titre']
    concert["heure_debut"] = request.form['heure_debut']
    concert["heure_duree"] = request.form['heure_duree']
    concert["minute_duree"] = request.form['minute_duree']
    concert["jour"] = 7
    CONCERTS.append(concert)
    return redirect(url_for('concert', nom=concert["nom"]))

# class AuthorForm(FlaskForm):
#     id = HiddenField('id')
#     name = StringField('name', validators=[DataRequired()])
# def save_author():
#     a = None
#     f = AuthorForm()
#     if f.validate_on_submit():
#         id = int(f.id.data)
#         a = get_author(id)d
#         a.name = f.name.data
#         db.session.commit()
#         return redirect(url_for('one_author', id=a.id))
#     a = get_author(int(f.id.data))
#     return render_template(
#         "edit-author.html",
#         author=a, form=f)

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