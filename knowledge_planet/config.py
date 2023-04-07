DEBUG = True
HOST = "0.0.0.0"
PORT = 9000
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://qt:123456@192.168.220.110:3306/KnowPlanet?charset=utf8'
SQLALCHEMY_TRACK_MODIFI = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

UPLOAD_FOLDER = '/data/nginx/html/files' # 上传文件保存的文件夹路径
FILE_URL = 'http://192.168.220.110/files/'
AVATAR_UPLOAD_FOLDER = '/data/nginx/html/avatar'
COMMENT_ATTACHMENT_UPLOAD_FOLDER = '/data/nginx/html/comment_attachment'
COMMENT_ATTACHMENT_URL = 'http://192.168.220.110/comment/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # 允许上传的文件类型
AVATAR_URL = 'http://192.168.220.110/avatar/'
# SQLALCHEMY_DATABASE_URI = 'mysql://qt:123456@192.168.220.110:3306/KnowPlanet'