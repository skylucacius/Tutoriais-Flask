from flask import Flask, url_for, render_template, send_from_directory, redirect, url_for, request, session
from werkzeug.utils import escape
# import os
# pastaRaiz = os.path.dirname(__file__)
# pastaTemplates = os.path.realpath(pastaRaiz + '/../frontend')
# pastaStatic = os.path.join(pastaTemplates, 'static')

app = Flask(__name__,template_folder='../frontend',static_folder='../frontend/static')
app.secret_key = '''_5#y2L"F4Q8z\n\xec]/'''

@app.route('/')
def padrao():
    return 'Hello World!'

@app.route('/pagina1/')
def paginaa1():
    return 'Olá página 1!'

@app.route('/pagina2/')
def paginaa2():
    print(url_for('paginaa1'))
    return redirect(url_for('paginaa1'))

@app.route('/pagina3/')
@app.route('/pagina3/<string:usuario>/')
def paginaa3(usuario=None):
    return 'Olá, ' + usuario if usuario else 'Olá'

@app.route('/pagina4/')
def paginaa4():
    return render_template('teste1.html')

@app.route('/pagina5/')
def index():
    if 'usuario' in session:
        string = '<p>logou como %s' % escape(session['usuario'])
        string += "</p><p><a href=" + url_for('logout') + "><button>Deslogar</button></a></p>"
        return string
    return "<p>Você não logou </p><a href='" + url_for('login') + "'><button>Logar</button></a> "

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['usuario'] = request.form['usuario']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=usuario>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('usuario', None)
    return redirect(url_for('index'))