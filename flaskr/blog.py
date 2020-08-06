from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import conecta

bp = Blueprint('blog', __name__)

@bp.route('/')
def index(): # retorna todos os posts na página principal
    db = conecta()
    posts = db.execute('SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@login_required
@bp.route('/create', methods=('GET', 'POST'))
def create_post(): # cria um novo post com título, corpo pelo id do autor
    if request.method == 'POST':
        titulo = request.form['titulo']
        corpo = request.form['corpo']
        erro = None

        if not titulo:
            erro = 'Título é necessário.'

        if erro is not None:
            flash(erro)
        else:
            db = conecta()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (titulo, corpo, g.usuario['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, checa_autor=True): # retorna um post (tupla) pelo id
    post = conecta().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post de id {0} não existe.".format(id))

    if checa_autor and post['author_id'] != g.usuario['id']:
        abort(403) # erro de falta de permissão

    return post

@login_required
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update_post(id): # atualiza um post por seu id
    post = get_post(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        corpo = request.form['corpo']
        erro = None

        if not titulo:
            erro = 'Título é necessário.'

        if erro is not None:
            flash(erro)
        else:
            db = conecta()
            db.execute('UPDATE post SET title = ?, body = ? WHERE id = ?',(titulo, corpo, id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@login_required
@bp.route('/<int:id>/delete', methods=['post'])
def delete_post(id): # delete o post pelo id
    post = get_post(id)
    db = conecta()
    db.execute('delete from post where id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))