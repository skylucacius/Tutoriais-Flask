from flask import Flask
app = Flask(__name__)

@app.route('/')
def padrao():
    return 'Hello World!'

@app.route('/pagina1/')
def paginaa1():
    return 'Olá página 1!'

@app.route('/pagina2/')
def paginaa2():
    return 'Olá página 2!'

@app.route('/pagina3/')
@app.route('/pagina3/<string:usuario>/')
def paginaa3(usuario=None):
    return 'Olá, ' + usuario if usuario else 'Olá'

