from flask import Flask, session, jsonify, request
from models import db, User

app = Flask(__name__)
app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Create database tables and add default user
with app.app_context():
    db.create_all()
    if not User.query.first():
        default_user = User(username="testuser")
        db.session.add(default_user)
        db.session.commit()

@app.route('/clear', methods=['GET'])
def clear_session():
    '''Clear the session'''
    session.clear()
    return '', 204

@app.route('/login', methods=['POST'])
def login():
    '''Log in a user'''
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    session['user_id'] = user.id
    return jsonify({
        'id': user.id,
        'username': user.username
    }), 200

@app.route('/logout', methods=['DELETE'])
def logout():
    '''Log out the current user'''
    session.pop('user_id', None)
    return '', 204

@app.route('/check_session', methods=['GET'])
def check_session():
    '''Check if a user is logged in'''
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({}), 401
    
    return jsonify({
        'id': user.id,
        'username': user.username
    }), 200