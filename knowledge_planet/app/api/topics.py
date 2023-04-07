from flask import Blueprint, request, jsonify
from ..models import db, Topic, Course
from .utils import auth_required
from .courses import courses_bp

topics_bp = Blueprint('topics',__name__,url_prefix="/api/v1/topics")


@auth_required
def create_topic(user_id):
    data = request.get_json()
    course_id = data.get('course_id')
    title = data.get('title')
    content = data.get('content')
    
    # 验证用户是否为课程所有者
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()
    if not course:
        return jsonify({'error': 'You are not authorized to perform this action'}), 401
    
    # 创建话题
    topic = Topic(course_id=course_id, user_id=user_id, title=title, content=content)
    db.session.add(topic)
    db.session.commit()
    
    return jsonify({'message': 'Topic created successfully'}), 201


def get_course_topics(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    topics = Topic.query.filter_by(course_id=course_id).all()
    result = []
    for topic in topics:
        topic_info = {
            'id': topic.id,
            'user_id': topic.user_id,
            'title': topic.title,
            'content': topic.content,
            'create_time': topic.create_time,
            'update_time': topic.update_time
        }
        result.append(topic_info)
    
    return jsonify(result)

@auth_required
def update_topic(user_id, topic_id):
    # 查询要更新的话题
    # topic = Topic.query.get_or_404(topic_id)
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({'error': 'topic not exists.'}), 404

    # 查询话题所在的课程
    # course = Course.query.get_or_404(topic.course_id)
    course = Course.query.get(topic.course_id)
    if not course:
        return jsonify({'error': 'course not exists.'}), 404

    # 检查当前用户是否是课程所有者
    if course.user_id != user_id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 401

    # 更新话题信息
    topic_data = request.get_json()
    title = topic_data.get('title')
    content = topic_data.get('content')
    if title:
        topic.title = title
    if content:
        topic.content = content
    db.session.commit()

    return jsonify({'success': 'Topic updated successfully'}), 200


@auth_required
def delete_topic(topic_id, user_id):
    # 判断该话题是否存在
    topic = Topic.query.filter_by(id=topic_id).first()
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    # 判断当前用户是否是该话题的创建者
    if topic.user_id != user_id:
        return jsonify({'error': 'You are not authorized to perform this action'}), 401
    db.session.delete(topic)
    db.session.commit()
    return jsonify({'message': 'Topic deleted successfully'}), 200

topics_bp.add_url_rule("/", view_func=create_topic, methods=["POST"])
courses_bp.add_url_rule("/<int:course_id>/topics", view_func=get_course_topics, methods=["GET"])
topics_bp.add_url_rule("/<int:topic_id>", view_func=update_topic, methods=["PUT"])
topics_bp.add_url_rule("/<int:topic_id>", view_func=delete_topic, methods=["DELETE"])
