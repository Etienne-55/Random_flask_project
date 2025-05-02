from flask import Flask, request, jsonify, render_template
from config import Config 
from flask_migrate import Migrate
from extensions import db
from flask_jwt_extended import JWTManager
from routes import register_routes_templates, register_routes 

migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    register_routes(app)
    register_routes_templates(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run (host='0.0.0.0', port=5000)
