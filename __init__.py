from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime, timedelta
import os.path
text = 'import worekd'
try:
    from lesson_handler import handle_lesson
except Exception as e:
    text = str(e)
from havefun import havefun

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databasetheshitoutofit.db'
db = SQLAlchemy(app)


class LessonModel(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)

#db.create_all()

minimal_fields = {
    'lesson_id': fields.Integer,
    'status': fields.Integer
}


class Status(Resource):
    def get(self):
        p = '/var/www/FlaskApp/FlaskApp/token'
        token_status = 'unacquired'
        if os.path.exists(p):
            t = os.path.getmtime(p)
            d = datetime.fromtimestamp(t)
            if datetime.now() - d < timedelta(hours=2):
                token_status = "up_to_date"
        return {"server_status": "running",
                "token_status": token_status}

class Lessons(Resource):
    @marshal_with(minimal_fields)
    def get(self):
        result = LessonModel.query.all()
        return result

    def delete(self):
        LessonModel.query.delete()
        return '', 204

class Lesson(Resource):
    @marshal_with(minimal_fields)
    def get(self, lesson_id):
        result = LessonModel.query.filter_by(lesson_id=lesson_id).first()
        if not result:
            abort(404, message="Lesson could not be found")
        return result

    @marshal_with(minimal_fields)
    def put(self, lesson_id):
        result = LessonModel.query.filter_by(lesson_id=lesson_id).first()
        if result:
            abort(409, message="Lesson id taken and " + havefun())
        lesson = LessonModel(lesson_id=lesson_id, status=0)
        db.session.add(lesson)
        db.session.commit()
        handle_lesson(db.session, LessonModel, lesson_id)
        return lesson, 201 #this ansewr will actually not send until we either signed up, are past due date or an error occurred, put requests will just time out, to fix this we need to start threads

    def delete(self, lesson_id):
        LessonModel.query.filter_by(lesson_id=lesson_id).delete()
        db.session.commit()
        return '', 204

api.add_resource(Lessons, "/lessons")
api.add_resource(Lesson, "/lessons/<int:lesson_id>")
api.add_resource(Status, "/status")

if __name__ == "__main__":
    app.run(debug=True)
