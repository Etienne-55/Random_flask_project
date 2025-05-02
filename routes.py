from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, current_user
from models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


def register_routes_templates(app):

    @app.route('/')
    def Landing_Page_Template():
        return render_template('landing_page.html')
    
    @app.route('/hello_raspberry')
    def Hello_Word_Raspberry():
        return "Hello world from raspberry"

    @app.route('/register')
    def RegisterUser_Template():
        return render_template('register.html')

    @app.route('/login')
    def Login_Template():
        return render_template('login.html')

    @app.route('/post_dashboard')
    def post_dashboard_template():
        return render_template('post_dashboard.html')


def register_routes(app):    
    @app.route('/register-user', methods=['POST'])
    def RegisterUser():
        data = request.get_json()

        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400

        hashed_password = generate_password_hash(data['password'])
        new_user = User(email=data['email'], password=hashed_password, is_admin=False)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    @app.route('/login-user', methods=['POST'])
    def Login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access token': access_token,
            'is_admin': user.is_admin,
        }), 200

    with app.app_context():
        db.create_all()

    @app.route('/posts', methods=['GET'])
    @jwt_required()
    def get_posts():
        current_user_id = get_jwt_identity()
        posts = Post.query.filter_by(user_id=current_user_id).order_by(Post.id.desc()).all()

        return jsonify([{
            'id': post.id,
            'content': post.content,
            'created_at': post.created_at.isoformat() if hasattr(post, 'created_at') else None,
            'user_id': post.user_id,
        } for post in posts]), 200

    @app.route('/posts', methods=['POST'])
    @jwt_required()
    def create_post():
        user_id = get_jwt_identity()
        data = request.get_json()

        new_post = Post(content=data['content'], user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({
            'message': 'Post created',
            'post': {
                'id': new_post.id,
                'content': new_post.content,
                'user_id': new_post.user_id,
                'created_at': new_post.created_at.isoformat() if hasattr(new_post, 'created_at') else None,
            }
        }), 201
