from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    avatar_url = db.Column(db.String(200))
    gender = db.Column(db.String(10))
    bio = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# class Lesson(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
#     name = db.Column(db.String(50), nullable=False)
#     content = db.Column(db.Text)
#     video_url = db.Column(db.String(255))
#     create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
#     update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    paragraphs = db.relationship('LessonParagraph', backref='lesson', lazy=True, cascade='all, delete-orphan')
    course = db.relationship('Course', backref='lesson', lazy=True)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class LessonParagraph(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'create_time': self.create_time,
            'update_time': self.update_time
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachment_url = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "topic_id": self.topic_id,
            "content": self.content,
            "attachment_url": self.attachment_url,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }

# class CommentAttachment(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
#     url = db.Column(db.String(200), nullable=False)
#     create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
#     update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    # 创建外键约束
    course = db.relationship('Course', backref=db.backref('tags', lazy=True))
    __table_args__ = (db.ForeignKeyConstraint([course_id], [Course.id]), {})
    

class TopicTag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())