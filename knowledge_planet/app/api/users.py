from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from ..models import db, User
from .utils import generate_token, auth_required, allowed_file
import os
import uuid
from flask import url_for
# from .. import run



users_bp = Blueprint('users',__name__,url_prefix="/api/v1/users")


@auth_required
def check_permission(user_id):
    if user_id:
        return  jsonify({"message": "auth successful."}), 200

def register():
    # 获取请求体中的用户名、邮箱、密码
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    # 判断用户名、邮箱是否已被注册
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "Username already exists!"}), 400
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "Email already exists!"}), 400
    # 将密码加密后保存到数据库中
    user = User(username=username, email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully."}), 201


def login():
    # 获取请求体中的用户名、邮箱、密码
    username_or_email = request.json.get("username_or_email")
    password = request.json.get("password")
    # 根据用户名或邮箱查询用户信息
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    # 如果用户不存在或密码错误，返回401状态码
    if user is None or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or email or password."}), 401
    # 登录成功，返回用户信息和token
    token = generate_token(user.id)  # 生成token，自行实现
    return jsonify({"user_id": user.id, "username": user.username, "email": user.email, "token": token}), 200


@auth_required
def alert_password(user_id):
    # 获取用户id和请求体中的旧密码和新密码
    # user_id = g.user_id
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")
    # 查询用户信息
    user = User.query.filter_by(id=user_id).first()
    # 如果用户不存在或旧密码错误，返回401状态码
    if user is None or not check_password_hash(user.password, old_password):
        return jsonify({"message": "Invalid user or old password."}), 401
    # 更新用户密码
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully."}), 200


def alert_profile():
    return 'this is alert_profile'


@auth_required
def upload_avatar(user_id):
    # 检查是否有上传的文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    
    # 检查文件类型是否为允许的图片类型
    if file and allowed_file(file.filename):
        # 生成一个唯一的文件名
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        new_filename = str(uuid.uuid4()) + ext
        
        # 保存文件到本地
        file.save(os.path.join(current_app.config['AVATAR_UPLOAD_FOLDER'], new_filename))
        
        # 更新用户头像链接
        user = User.query.filter_by(id=user_id).first()
        if user:
            # user.avatar_url = url_for('uploaded_file', filename=new_filename, _external=True)
            user.avatar_url = new_filename
            db.session.commit()
            return jsonify({'avatar_url': user.avatar_url}), 200
        
    return jsonify({'error': 'Invalid file type or file not saved'}), 400

# 查看当前用户信息
@auth_required
def get_user_info(user_id):
    user = User.query.get(user_id)
    return jsonify({
        'username': user.username,
        'email': user.email,
        'avatar_url': current_app.config['AVATAR_URL']+user.avatar_url,
        'gender': user.gender,
        'bio': user.bio,
    })

def get_specific_user_info(user_id):
    user = User.query.get(user_id)
    return jsonify({
        'username': user.username,
        'email': user.email,
        'avatar_url': user.avatar_url,
        'gender': user.gender,
        'bio': user.bio,
    })

@auth_required
def update_user_info(user_id):
    # 获取请求中的参数
    gender = request.json.get('gender')
    bio = request.json.get('bio')
    # 获取当前登录的用户信息
    current_user = User.query.get(user_id)
    # 如果当前登录的用户不存在，则返回错误信息
    if not current_user:
        return jsonify({'error': 'user not found'}), 404
    # 如果请求中传入了新的性别，则更新用户的性别
    if gender is not None:
        current_user.gender = gender
    # 如果请求中传入了新的个签，则更新用户的个签
    if bio is not None:
        current_user.bio = bio
    # 将修改后的用户信息保存到数据库中
    db.session.commit()
    # 返回修改后的用户信息
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'gender': current_user.gender,
        'bio': current_user.bio,
        'avatar_url': current_user.avatar_url
    })
    
    
# 注册
users_bp.add_url_rule("/", view_func=register, methods=["POST"])
# 登录
users_bp.add_url_rule("/login", view_func=login, methods=["POST"])
# 改密码
users_bp.add_url_rule("/password", view_func=alert_password, methods=["PUT"])
# users_bp.add_url_rule("/profile", view_func=alert_profile, methods=["PUT"])
# 设置头像
users_bp.add_url_rule("/avatar", view_func=upload_avatar, methods=["POST"])
# 获取当前用户的信息
users_bp.add_url_rule("/current", view_func=get_user_info, methods=["GET"])
# 获取指定用户的信息
users_bp.add_url_rule("/<int:user_id>", view_func=get_specific_user_info, methods=["GET"])
# 修改当前用户的信息
users_bp.add_url_rule("/", view_func=update_user_info, methods=["PUT"])

users_bp.add_url_rule("/check", view_func=check_permission, methods=["GET"])