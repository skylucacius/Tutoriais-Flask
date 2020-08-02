import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import conecta

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # get : irá se registrar
    # post: registra
    if request.method == 'POST':
        login = request.form['usuario']
        senha = request.form['senha']
        db = conecta()
        erro = None

        if not login:
            erro = 'Nome de usuário é necessário.'
        elif not senha:
            erro = 'Senha é necessária.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (login,)).fetchone() is not None:
            erro = 'Usuário {} já está registrado.'.format(login)

        if erro is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                (login, generate_password_hash(senha)))
            
            db.commit()
            return redirect(url_for('auth.login'))

        flash(erro)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    # get: irá se logar
    # post: efetua o login
    if request.method == 'POST':
        login = request.form['usuario']
        senha = request.form['senha']
        db = conecta()
        erro = None
        usuario = db.execute('select * from user where username = ?', (login,)).fetchone()

        if not login:
            erro = 'Usuário é necessário.'
        elif not check_password_hash(usuario['password'], senha):
            erro = 'Senha é necessária.'

        if erro is None:
            session.clear()
            session['id'] = usuario['id']
            return redirect(url_for('index'))

        flash(erro)        

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_request 
def carrega_usuario_logado(): # decorador que retorna o estado de login do usuário
    if session['id'] is not None:
        id_usuario = session.get('id')
        if id_usuario is None:
            g.usuario = None
        else:
            g.usuario = conecta().execute('select * from user where id = ?', (id_usuario,)).fetchone()
