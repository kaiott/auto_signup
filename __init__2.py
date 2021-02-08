from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, abort, fields, marshal_with
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class LessonModel(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)

#db.create_all()

minimal_fields = {
    'lesson_id': fields.Integer,
    'status': fields.Integer
}

@app.route("/")
def hello():
    try:
        LessonModel.query.delete()
        db.session.commit()
        return 'successfully delete db'
    except Exception as e:
        return f'could not delete db : {str(e)}'

@app.route("/lessons")
@marshal_with(minimal_fields)
def test():
    result = LessonModel.query.all()
    if result is None:
        return 'skdfljaf'
    return result[1]

@app.route("/lessons/<int:lesson_id>", methods=['GET'])
@marshal_with(minimal_fields)
def get(lesson_id):
    result = LessonModel.query.filter_by(lesson_id=lesson_id).first()
    if not result:
        abort(404, message="Lesson could not be found")
    return result
@app.route("/lessons/<int:lesson_id>", methods=['PUT'])
#@marshal_with(minimal_fields)
def put(lesson_id):
    lesson_id = int(lesson_id)
    result = LessonModel.query.filter_by(lesson_id=lesson_id).first()
    if result:
        #abort(409, message="Lesson id taken")
        return f'already taken by {result.lesson_id}'
    lesson = LessonModel(lesson_id=lesson_id, status=0)
    db.session.add(lesson)
    try:
        #1/0
        db.session.commit()
        return 'success'
    except Exception as e:
        return str(e)
@app.route("/lessons/<int:lesson_id>", methods=['DELETE'])
def delete(lesson_id):
    return f'deleted lesson {lesson_id}'
@app.route("/test", methods=['POST'])
def test_post():
    return "Posted"
@app.route("/<name>")
def love(name):
    return f"and you too{name}"
@app.route("/test2")
def test2():
   return "this sould never be visible"
if __name__ == "__main__":
    app.run()
