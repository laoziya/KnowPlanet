from .topics import topics_bp
from .courses import courses_bp
from .topics import topics_bp
from ..models import db, Tag, TopicTag, Course, Topic
from flask import Blueprint, request, jsonify
from .utils import auth_required


tags_bp = Blueprint('tags',__name__,url_prefix="/api/v1/tags")


@auth_required
def create_tag(user_id):
    course_id = request.json.get('course_id')
    name = request.json.get('name')
    if not course_id or not name:
        return jsonify({'error': 'Missing required parameters'}), 400
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()
    if not course:
        return jsonify({'error': 'Course not found or you are not authorized to perform this action'}), 404
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        tag = Tag(name=name, course_id=course_id)
        db.session.add(tag)
        db.session.commit()
        return jsonify({'id': tag.id, 'name': tag.name}), 201
    return jsonify({'error': 'tag is exist.'}), 403
    # topic_tag = TopicTag.query.filter_by(topic_id=None, tag_id=tag.id).first()
    # if not topic_tag:
    #     topic_tag = TopicTag(tag_id=tag.id)
    #     db.session.add(topic_tag)
    # db.session.commit()
    


def get_course_tags(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course does not exist'}), 404

    tags = Tag.query.filter(Tag.course_id == course_id).all()
    tag_list = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return jsonify({'tags': tag_list})


@auth_required
def add_topic_tag(user_id, topic_id, tag_id):
    topic = Topic.query.get(topic_id)
    tag = Tag.query.get(tag_id)
    if not tag or not topic:
        return jsonify({'error': 'no this tag or t.'}), 404
    if tag.course.user_id != user_id:
        return jsonify({'error': 'Only course owner can add tag to topic.'}), 403

    if not topic:
        return jsonify({'error': 'Topic does not exist'}), 404
    if not tag:
        return jsonify({'error': 'Tag does not exist'}), 404

    topic_tag = TopicTag.query.filter_by(topic_id=topic_id, tag_id=tag_id).first()
    if topic_tag:
        return jsonify({'error': 'Tag already added to topic'}), 400

    topic_tag = TopicTag(topic_id=topic_id, tag_id=tag_id)
    db.session.add(topic_tag)
    db.session.commit()

    return jsonify({'message': 'Tag added to topic successfully'}), 201

def get_topic_tags(topic_id):
    # 查询话题是否存在
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({'message': 'Topic not found'}), 404
    # 查询话题关联的标签
    tags = Tag.query.join(TopicTag, Tag.id == TopicTag.tag_id).filter(TopicTag.topic_id == topic_id).all()
    # 构造返回的标签列表
    tag_list = []
    for tag in tags:
        tag_list.append({
            'id': tag.id,
            'name': tag.name,
            'create_time': tag.create_time,
            'update_time': tag.update_time
        })
    return jsonify(tag_list)

# 更新标签
@auth_required
def update_tag(tag_id, user_id):
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'message': 'Tag not found'}), 404
    # 只有创建标签的用户才有权限更新标签
    if tag.course.user_id != user_id:
        return jsonify({'message': 'Permission denied'}), 403
    # 从请求体中获取要更新的字段
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON request body'}), 400
    name = data.get('name')
    if not name:
        return jsonify({'message': 'Name is required'}), 400
    # 更新标签
    tag.name = name
    db.session.commit()
    return jsonify({'message': 'Tag updated successfully'})


# 删除标签
@auth_required
def delete_tag(user_id, tag_id):
    # 检查标签是否存在
    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'message': 'Tag not found'}), 404
    # 检查当前用户是否有删除权限
    if user_id != tag.course.user_id:
        return jsonify({'message': 'Unauthorized to delete the tag'}), 403
    # 删除标签
    # 删除所有使用了这个标签的话题记录
    topic_tags = TopicTag.query.filter_by(tag_id=tag_id).all()
    for topic_tag in topic_tags:
        db.session.delete(topic_tag)
    db.session.delete(tag)
    db.session.commit()
    
    return jsonify({'message': 'Tag deleted successfully'}), 200

def get_topics_by_tag(tag_id):
    topic_tags = db.session.query(TopicTag).filter_by(tag_id=tag_id).all()
    topic_ids = [topic_tag.topic_id for topic_tag in topic_tags]
    topics = db.session.query(Topic).join(TopicTag).filter(TopicTag.topic_id.in_(topic_ids)).all()
    return jsonify([topic.to_dict() for topic in topics])

# @app.route('/topics/<int:topic_id>/tags', methods=['GET'])
courses_bp.add_url_rule("/tags", view_func=create_tag, methods=["POST"])
courses_bp.add_url_rule("/<int:course_id>/tags", view_func=get_course_tags, methods=["GET"])
topics_bp.add_url_rule("/<int:topic_id>/tags/<int:tag_id>", view_func=add_topic_tag, methods=["POST"])
topics_bp.add_url_rule("/<int:topic_id>/tags", view_func=get_topic_tags, methods=["GET"])
tags_bp.add_url_rule("/<int:tag_id>", view_func=update_tag, methods=["PUT"])
tags_bp.add_url_rule("/<int:tag_id>", view_func=delete_tag, methods=["DELETE"])
topics_bp.add_url_rule("/tags/<int:tag_id>", view_func=get_topics_by_tag, methods=["GET"])