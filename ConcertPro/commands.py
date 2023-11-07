from .models import *
import click
from .app import app

# @app.cli.command()
# @click.argument('filename')

@app.cli.command()
@click.argument('req')
def requete(req):
    try:
        cursor.execute(req)
        info = cursor.fetchall()
        for i in info:
            print(i)
    except Exception as e:
        print(e.args)
