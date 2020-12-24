import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def conecta():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def fecha(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def cria_tabelas():
    db = conecta()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('cria-banco')
@with_appcontext
def cli_cria_tabelas():
    """abre o banco cria as tabelas"""
    cria_tabelas()
    click.echo('Banco de dados aberto.')

# não temos a instância do app aqui, logo devemos abstrair que a temos e que poderemos usar seus métodos
def iniciar(app):
    app.teardown_appcontext(fecha)
    app.cli.add_command(cli_cria_tabelas)
