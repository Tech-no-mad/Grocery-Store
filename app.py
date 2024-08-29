import os
from flask import Flask
from Admin.authadmin import authA
from User.authuser import authU
from StoreManager.authmanager import authM
from models import db

def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    app.secret_key = "hello"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(authU)
    app.register_blueprint(authM)
    app.register_blueprint(authA)
    

    if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
    return app


create_app()
