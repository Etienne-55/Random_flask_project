from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from models import User
from config import Config 
from flask_migrate import Migrate
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

migrate = Migrate()
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
    
    @app.route('/register-user', methods=['POST'])
    def RegisterUser():
        data = request.get_json()

        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(email=data['email'], password=hashed_password, is_admin=False)

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    @app.route('/login', methods=['POST'])
    def Login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return{'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=str(user.id))
        return{
            'access token': access_token,
        }, 200

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run (host='0.0.0.0', port=5000)
