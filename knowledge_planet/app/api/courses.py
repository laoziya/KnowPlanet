from flask import Blueprint, request, jsonify
from ..models import db, Course
from .utils import auth_required    
from .users import users_bp

courses_bp = Blueprint('courses',__name__,url_prefix="/api/v1/courses")


@auth_required
def create_course(user_id):
    # 获取请求体中的参数
    title = request.json.get('title')
    description = request.json.get('description')
    
    # 构造课程对象
    course = Course(user_id=user_id, title=title, description=description)
    
    # 将课程对象保存到数据库中
    db.session.add(course)
    db.session.commit()
    
    # 返回添加成功的课程信息
    return jsonify({'id': course.id, 'user_id': course.user_id, 'title': course.title, 'description': course.description})



def get_all_courses():
    courses = Course.query.all()
    result = []
    for course in courses:
        course_data = {}
        course_data['id'] = course.id
        course_data['user_id'] = course.user_id
        course_data['title'] = course.title
        course_data['description'] = course.description
        course_data['create_time'] = course.create_time.strftime("%Y-%m-%d %H:%M:%S")
        course_data['update_time'] = course.update_time.strftime("%Y-%m-%d %H:%M:%S")
        result.append(course_data)
    return jsonify(result)

from flask import jsonify


def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify({
        'id': course.id,
        'user_id': course.user_id,
        'title': course.title,
        'description': course.description,
        'create_time': course.create_time,
        'update_time': course.update_time
    })

def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    title = data.get('title')
    description = data.get('description')
    
    if title:
        course.title = title
    if description:
        course.description = description
    
    db.session.commit()
    
    return jsonify({'message': 'Course updated successfully'})

@auth_required
def update_course(id, user_id):
    course = Course.query.get_or_404(id)

    # 只有课程所有者才能修改课程信息
    if course.user_id != user_id:
        return jsonify({'error': 'Only course owner can update the course.'}), 403

    # 更新课程信息
    if 'title' in request.json:
        course.title = request.json['title']
    if 'description' in request.json:
        course.description = request.json['description']
    db.session.commit()

    return jsonify({'message': 'Course updated successfully.'})


def get_user_courses(user_id):
    courses = Course.query.filter_by(user_id=user_id).all()
    courses_list = [{'id': c.id, 'title': c.title, 'description': c.description, 'create_time':c.create_time, } for c in courses]
    return jsonify(courses_list)

@auth_required
def get_current_user_courses(user_id):
    courses = Course.query.filter_by(user_id=user_id).all()
    courses_list = [{'id': c.id, 'title': c.title, 'description': c.description, 'create_time':c.create_time, } for c in courses]
    return jsonify(courses_list)

@auth_required
def delete_course(course_id, user_id):
    # 获取要删除的课程
    course = Course.query.filter_by(id=course_id).first()
    # 如果找不到对应的课程，返回404错误
    if not course:
        return jsonify({'message': 'No such course.'}), 404
    # 如果用户不是课程的所有者，返回403错误
    if course.user_id != user_id:
        return jsonify({'message': 'Invalid token'}), 403
    # 删除课程
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully.'})


courses_bp.add_url_rule('/', view_func=create_course, methods=["POST"])
courses_bp.add_url_rule('/', view_func=get_all_courses, methods=["GET"])
courses_bp.add_url_rule('/<int:id>', view_func=get_course, methods=["GET"])
courses_bp.add_url_rule('/<int:id>', view_func=update_course, methods=["PUT"])
users_bp.add_url_rule('/<int:user_id>/courses', view_func=get_user_courses, methods=["GET"])
users_bp.add_url_rule('/courses', view_func=get_current_user_courses, methods=["GET"])
courses_bp.add_url_rule('/<int:course_id>', view_func=delete_course, methods=["DELETE"])