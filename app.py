from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/users.db'

# 配置CORS
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "https://codecenter1024.github.io"}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 邀请码配置
VALID_INVITE_CODES = {'TECHBLOG2024', 'HANZHEBLOG'}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    invite_code = db.Column(db.String(20), nullable=False)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('invite_code') or data['invite_code'] not in VALID_INVITE_CODES:
        return jsonify({'error': '无效邀请码'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password=hashed_password,
        invite_code=data['invite_code']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        session['user_id'] = user.id
        return jsonify({'message': '登录成功'})
    return jsonify({'error': '用户名或密码错误'}), 401

@app.route('/api/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': '已退出登录'})

@app.route('/api/post', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return jsonify({'error': '需要登录'}), 401
    
    data = request.json
    # 保存文章到articles目录
    filename = f"articles/{data['title'].replace(' ', '_')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data['content'])
    
    return jsonify({'message': '文章发布成功', 'path': filename})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)