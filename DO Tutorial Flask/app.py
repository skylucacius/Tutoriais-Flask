from flask import Flask, render_template
from os.path import realpath, dirname, join
import sqlite3

app = Flask(__name__ ,template_folder="frontend/templates", static_folder="frontend/static")
path_db = join(dirname(realpath(__file__)), 'database.db')

def connection():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row
    return conn

def getPosts():
    lista = connection().execute('select * from posts').fetchall()
    connection().close()
    return lista


@app.route('/') 
def index():
    posts = getPosts()
    return render_template('index.html', posts=posts)
