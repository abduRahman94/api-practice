import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})


class Student(db.Model):
    __tablename__='students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    program = db.Column(db.String(100))
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'program': self.program,
        }

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', True)
    return response


@app.route('/api/students', methods=['GET', 'POST'])
@cross_origin()
def students():
    if request.method == 'GET':
        students = [student.format() for student in Student.query.all()]
        return jsonify({'students': students})
    
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        program = data.get('program')
        
        student = Student(name=name, surname=surname, program=program)
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'id': student.id,
            'message': 'Created successfully'
        })

@app.route('/api/students/<int:id>', methods=['GET'])
def student(id):
    try:
        student = Student.query.get(id)
        return jsonify(student.format())
    except AttributeError:
        return jsonify({
            'message': 'Student does\'t exist'
        }), 404

@app.route('/api/students/<int:id>', methods=['PUT', 'PATCH'])
def update_student(id):
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        surname = data.get('surname')
        program = data.get('program')
        
        try:
            student = Student.query.get(id)
            student.name = name
            student.surname = surname
            student.program = program
            # db.session.add(student)
            db.session.commit()
            return jsonify({
                'id': student.id,
                'message': 'Updated successfully'
            })
        except AttributeError:
            return jsonify({
            'message': 'Student does\'t exist'
        }), 404


@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({
            'id': student.id,
            'message': 'Deleted successfully'
        })
    except AttributeError:
        return jsonify({
            'message': 'Student does\'t exist'
        }), 404


@app.errorhandler(404)
def not_found():
    return jsonify({
        'error': 404,
        'message': '404 Not found'
    })

@app.errorhandler(500)
def not_found():
    return jsonify({
        'error': 500,
        'message': 'Internal Server Error'
    })