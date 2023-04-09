import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
# from .. import run



# 生成 token 的函数
def generate_token(user_id):
    # 设置 token 的有效期为 1 天
    expiration_time = datetime.utcnow() + timedelta(days=1)
    # 构建 token 的 payload（载荷）
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    # 使用 JWT 库生成 token
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    return token

# def auth_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         # 从请求头中获取 token
#         token = request.headers.get('Authorization')
#         if not token:
#             # 如果 token 不存在，返回 401 状态码
#             return jsonify({'message': 'Authorization required'}), 401
#         try:
#             # 验证 token 是否正确，如果正确解码并获取用户信息
#             payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
#             user_id = payload['user_id']
#             # 将 user_id 添加到函数参数中，以便后续函数调用
#             kwargs['user_id'] = user_id
#         except jwt.exceptions.InvalidSignatureError:
#             # 如果 token 不正确，返回 401 状态码
#             return jsonify({'message': 'Invalid token'}), 401
#         # 如果 token 验证通过，调用函数
#         return f(*args, **kwargs)
#     return decorated_function

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头中获取 token
        token = request.headers.get('Authorization')
        if not token:
            # 如果 token 不存在，返回 401 状态码
            return jsonify({'error': 'Authorization required'}), 401
        try:
            # 验证 token 是否正确，如果正确解码并获取用户信息
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            user_id = payload['user_id']
            # 检查证书是否在有效期内
            if 'exp' not in payload:
                return jsonify({'error': 'Invalid token'}), 401
            expiration_time = datetime.fromtimestamp(payload['exp'])
            if datetime.utcnow() > expiration_time:
                return jsonify({'error': 'Token has expired'}), 401
            # 将 user_id 添加到函数参数中，以便后续函数调用
            kwargs['user_id'] = user_id
        except jwt.exceptions.InvalidSignatureError:
            # 如果 token 不正确，返回 401 状态码
            return jsonify({'error': 'Invalid token'}), 401
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'ExpiredSignatureError'}), 401
        # 如果 token 验证通过，调用函数
        except:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated_function


# 检查上传的文件是否符合要求
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']