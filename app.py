from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

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
