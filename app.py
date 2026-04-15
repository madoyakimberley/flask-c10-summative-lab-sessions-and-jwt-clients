from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

from config import Config
from models import db, bcrypt, User, Note
import models 
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# AUTH ----> I shld have broken the code down but this will do
#TODO: BREAK DOWN THE CODE LATER ON

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return {"error": "Missing fields"}, 400

    if User.query.filter_by(username=data['username']).first():
        return {"error": "Username already exists"}, 400

    user = User(username=data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return {"message": "User created"}, 201

#Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()

    if not user or not user.check_password(data.get('password')):
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity=str(user.id))

    return {"access_token": token}, 200


@app.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    return {
        "id": user.id,
        "username": user.username
    }, 200


#NOTES 

@app.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    per_page = 5

    notes = Note.query.filter_by(user_id=user_id)\
        .paginate(page=page, per_page=per_page)

    return {
        "notes": [
            {
                "id": n.id,
                "title": n.title,
                "content": n.content
            } for n in notes.items
        ],
        "page": page,
        "total_pages": notes.pages
    }, 200


@app.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return {"error": "Missing fields"}, 400

    note = Note(
        title=data['title'],
        content=data['content'],
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return {"message": "Note created"}, 201


@app.route('/notes/<int:id>', methods=['PATCH'])
@jwt_required()
def update_note(id):
    user_id = get_jwt_identity()
    note = Note.query.get(id)

    if not note:
        return {"error": "Not found"}, 404

    if note.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    data = request.get_json()

    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)

    db.session.commit()

    return {"message": "Updated"}, 200


@app.route('/notes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_note(id):
    user_id = get_jwt_identity()
    note = Note.query.get(id)

    if not note:
        return {"error": "Not found"}, 404

    if note.user_id != user_id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(note)
    db.session.commit()

    return {"message": "Deleted"}, 200


if __name__ == '__main__':
    app.run(debug=True)