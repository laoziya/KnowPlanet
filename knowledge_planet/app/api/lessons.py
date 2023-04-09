from flask import Blueprint, request, jsonify, current_app
from .utils import auth_required
from ..models import db, Lesson, Course, LessonParagraph
from .courses import courses_bp
from werkzeug.utils import secure_filename
import os
import uuid

lessons_bp = Blueprint('lessons',__name__,url_prefix="/api/v1/lessons")


# 创建课时
@auth_required
def create_lesson(user_id):
    course_id = request.json.get('course_id')
    name = request.json.get('name')
    
    # 验证用户是否有权创建该课时
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()
    if course is None:
        return jsonify({'error': 'No permission to create lesson in the course.'}), 403

    # 创建课时
    lesson = Lesson(course_id=course_id, name=name)
    db.session.add(lesson)
    db.session.commit()
    lesson_id = lesson.id

    paragraph = LessonParagraph(lesson_id=lesson_id, content='[内容为空]')
    db.session.add(paragraph)
    db.session.commit()

    return jsonify({'id': lesson.id}), 201


@auth_required
def add_lesson_paragraph(user_id, lesson_id):
    # 验证用户是否有权编辑该课时
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    if lesson is None:
        return jsonify({'error': 'Lesson not found.'}), 404
    if lesson.course.user_id != user_id:
        return jsonify({'error': 'No permission to edit lesson.'}), 403
    # 获取请求参数
    content = request.json.get('content')
    name = request.json.get('name')
    lesson.name = name
    paragraphs = LessonParagraph.query.filter_by(lesson_id=lesson.id).all()
    for paragraph in paragraphs:
        db.session.delete(paragraph)
        
    # 创建段落
    paragraph = LessonParagraph(lesson_id=lesson_id, content=content)
    db.session.add(paragraph)
    db.session.commit()

    return jsonify({'id': paragraph.id}), 201

def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file submitted"}), 400
    file = request.files['file']

    # 保存文件到服务器
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1]
    new_filename = str(uuid.uuid4()) + ext
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
    file_url = current_app.config['FILE_URL']+new_filename
    # 返回url
    return jsonify({'file_url': file_url})

# 获取一个课程中所有的Lesson
def get_lessons_by_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    lessons = Lesson.query.filter_by(course_id=course_id).all()

    result = []
    for lesson in lessons:
        lesson_data = {
            'id': lesson.id,
            'course_id': lesson.course_id,
            'name': lesson.name,
        }
        result.append(lesson_data)
    return jsonify(result), 200

# 获取一个Lesson的详细内容
def get_lesson_info(lesson_id):
    lesson = Lesson.query.get(lesson_id)    
    if not lesson:
        return jsonify({'message': 'Lesson not found.'}), 404
    course = Course.query.get(lesson.course_id)
    return jsonify({
        'id': lesson.id,
        'course_id': lesson.course_id,
        'course_title': course.title,
        'name': lesson.name,
        'content': lesson.content,
        'video_url': lesson.video_url,
        'create_time': lesson.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'update_time': lesson.update_time.strftime('%Y-%m-%d %H:%M:%S')
    })

# 获取课时的详细信息
def get_lesson_detail(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    if not lesson:
        return jsonify({'message': 'Lesson not found.'}), 404
    paragraphs = LessonParagraph.query.filter_by(lesson_id=lesson.id).first()
    return jsonify({
        'id': lesson.id,
        'name': lesson.name,
        # 'paragraphs': [p.content for p in paragraphs],
        'content': paragraphs.content,
        'create_time': lesson.create_time.isoformat(),
        'update_time': lesson.update_time.isoformat(),
    })
    

# # 更改课时信息
# # @app.route('/lessons/<int:lesson_id>', methods=['PUT'])
# @auth_required
# def update_lesson(lesson_id, user_id):
#     lesson = Lesson.query.get(lesson_id)
#     if not lesson:
#         return jsonify({'error': 'Lesson not found'}), 404
    
#     course = Course.query.get(lesson.course_id)
#     if not course:
#         return jsonify({'error': 'Course not found'}), 404
    
#     if course.user_id != user_id:
#         return jsonify({'error': 'You are not authorized to perform this action'}), 401
    
#     request_data = request.get_json()
#     if 'name' in request_data:
#         lesson.name = request_data['name']
#     if 'content' in request_data:
#         lesson.content = request_data['content']
#     if 'video_url' in request_data:
#         lesson.video_url = request_data['video_url']

#     db.session.commit()

#     return jsonify({'success': 'Lesson updated successfully'}), 200



def delete_lesson(lesson_id):
    lesson = Lesson.query.get(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    db.session.delete(lesson)
    db.session.commit()
    return jsonify({'message': 'Lesson deleted successfully'})


# 新建课时
lessons_bp.add_url_rule("/", view_func=create_lesson, methods=["POST"])
# 编辑课时内容
lessons_bp.add_url_rule("/<int:lesson_id>/edit", view_func=add_lesson_paragraph, methods=["POST"])
# 上传文件
lessons_bp.add_url_rule("/file", view_func=upload_file, methods=["POST"])
# 获取一个课程中所有的课时
courses_bp.add_url_rule("/<int:course_id>/lessons", view_func=get_lessons_by_course, methods=["GET"])
# 获取一个课时的详情
lessons_bp.add_url_rule("/<int:lesson_id>", view_func=get_lesson_detail, methods=["GET"])
# 删除一个课程
lessons_bp.add_url_rule("/<int:lesson_id>", view_func=delete_lesson, methods=["DELETE"])
# lessons_bp.add_url_rule("/<int:lesson_id>", view_func=update_lesson, methods=["PUT"])
# lessons_bp.add_url_rule("/<int:lesson_id>", view_func=delete_lesson, methods=["DELETE"])
