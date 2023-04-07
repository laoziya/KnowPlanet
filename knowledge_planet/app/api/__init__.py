# from .study import stu_bp
# from .user import  user_bp
from .users import users_bp
from .courses import courses_bp
from .lessons import lessons_bp
from .topics import topics_bp
from .tags import tags_bp
from .comments import comments_bp



def init_app(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(topics_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(comments_bp)
    



