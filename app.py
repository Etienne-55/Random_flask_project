from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config 
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    @app.route('/')
    def hello():
        return "Hello World from rapsberry" 

    @app.route('/first-route')
    def first_route():
        return "testinf route"

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run (host='0.0.0.0', port=5000)
