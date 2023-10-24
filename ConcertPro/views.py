from flask import render_template
from .app import app

@app.route('/')
def accueil():
    return render_template(
        "accueil.html"
    )