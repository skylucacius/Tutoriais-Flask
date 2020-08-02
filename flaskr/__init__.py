import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'))

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except Exception as erro:
        print('O erro é', str(erro))
    
    @app.route('/')
    def index():
        return 'Hello World!'
    
    from . import db; db.iniciar(app) # a instância do banco abstraída na classe db.py será usada aqui
    from . import auth;app.register_blueprint(auth.bp)
    return app
