from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
try:
    api = Api(app)
except Exception as e:
    with open('logfile', 'a') as file:
        file.write('0' + str(e))

names = {"tim": {"age": 19, "gender": "male"},
        "sara": {"age": 20, "gender": "female"}}

class HelloWorld(Resource):
    def get(self, name):
        print('hi')
        if name in names:
            return names[name]
        return f'{name} not in database'


try:
    api.add_resource(HelloWorld, "/helloworld/<string:name>")
except Exception as e:
    with open('logfile', 'a') as file:
        file.write('0' + str(e))

if __name__ == "__main__":
    app.run(debug=True)

