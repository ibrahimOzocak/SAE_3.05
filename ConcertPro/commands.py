from . import models as mo
import click
from .app import app

# @app.cli.command()
# @click.argument('filename')

@app.cli.command()
@click.argument('req')
def requete(req):
    try:
        cursor = mo.get_cursor()
        cursor.execute(req)
        info = cursor.fetchall()
        mo.close_cursor(cursor)
        for i in info:
            print(i)
    except Exception as e:
        print(e.args)
