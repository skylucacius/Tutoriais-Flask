from flask import Flask, render_template, request, url_for, flash, redirect
from os.path import realpath, dirname, join
from werkzeug.exceptions import abort
import sqlite3

app = Flask(__name__ ,template_folder="frontend/templates", static_folder="frontend/static")
path_db = join(dirname(realpath(__file__)), 'database.db')
app.config['SECRET_KEY'] = 'cf9d8f2015e81df1a6f28daa181bed9e'

def connection():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row
    return conn

def printPosts():
    posts = getPosts()
    for post in posts:
        print("id: " + str(post["id"]) + ", data de criação: " + str(post["created"]) + ", título: " + 
        str(post["title"]) + ", conteúdo: " + str(post["content"]))

def getPosts():
    lista = connection().execute('select * from posts').fetchall()
    connection().close()
    return lista

def get_post(post_id):
    conn = connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def newPost(title,content):
    con = connection()
    con.execute('insert into posts (title,content) values (?,?)', (title, content))
    con.commit();con.close()

def updatePost(id,title,content):
    con = connection()
    con.execute('update posts set title = ?, content = ? where id = ?', (title, content, id))
    con.commit();con.close()

def deletePost(id):
    con = connection()
    con.execute('delete from posts where id = (?)', (id,))
    con.commit();con.close()

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("{} was successfully deleted!".format(post['title']))
    return redirect(url_for('index'))

@app.route('/') 
def index():
    posts = getPosts()
    return render_template('index.html', posts=posts)




# antes de construir a aplicação, alguns métodos CRUD foram implementados e testados. 
# Foi necessário editar o settings.json de modo a debugar rapidamente a aplicação. 
# A tabela posts tem as seguintes colunas: id, created, title, content. Então, temos:
# newPost('titulo 3', 'conteudo do post 3')
# updatePost(1, 'titulo do post 1 alterado', 'conteudo do post 1 alterado')
# deletePost(3)
# printPosts()