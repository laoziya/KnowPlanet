from .topics import topics_bp
from .courses import courses_bp
from .topics import topics_bp
from ..models import db, Tag, TopicTag, Course, Topic, Comment
from .utils import auth_required
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

comments_bp = Blueprint('comments',__name__,url_prefix="/api/v1/comments")


@auth_required
def create_comment(topic_id, user_id):
    print("create_comment")
    # 获取请求中的数据
    comment_data = request.json

    # 创建新的评论对象，并将其与话题关联起来
    new_comment = Comment(
        topic_id=topic_id,
        user_id=user_id, 
        content=comment_data['content']
    )

    # 将评论数据保存到数据库中
    db.session.add(new_comment)
    db.session.commit()

    # 返回保存的评论数据
    return jsonify(new_comment.to_dict())

def get_topic_comments(topic_id):
    comments = Comment.query.filter_by(topic_id=topic_id).all()
    if not comments:
        return jsonify({'message': 'No comments found for this topic'}), 404

    result = []
    for comment in comments:
        result.append(comment.to_dict())

    return jsonify(result), 200


@auth_required
def add_attachment_to_comment(comment_id, user_id):
    # 获取请求中的数据和文件
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    if comment.user_id != user_id:
        return jsonify({"error": "Only comment creator can add attachment to the comment"}), 403
    if 'file' not in request.files:
        return jsonify({"error": "No file submitted"}), 400
    file = request.files['file']

    # 保存文件到服务器
    filename = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['COMMENT_ATTACHMENT_UPLOAD_FOLDER'], filename))
    attachment_url = current_app.config['COMMENT_ATTACHMENT_URL']+filename

    # 更新评论对象
    comment.attachment_url = attachment_url
    db.session.commit()

    # 返回更新后的评论对象
    return jsonify(comment.to_dict())


topics_bp.add_url_rule("/<int:topic_id>/comments", view_func=create_comment, methods=["POST"])
topics_bp.add_url_rule("/<int:topic_id>/comments", view_func=get_topic_comments, methods=["GET"])
comments_bp.add_url_rule("/<int:comment_id>/attachments", view_func=add_attachment_to_comment, methods=["POST"])