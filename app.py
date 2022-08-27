import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        students = [student.format() for student in Student.query.all()]
        
        return jsonify({'students': students})
    
    if request.method == 'POST':
        name = request.form.get('name', None)
        surname = request.form.get('surname', None)
        program = request.form.get('program', None)
        
        student = Student(name=name, surname=surname, program=program)
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'id': student.id,
            'message': 'Created successfully'
        })

@app.route('/students/<int:id>', methods=['GET'])
def student(id):
    try:
        student = Student.query.get(id)
        return jsonify(student.format())
    except AttributeError:
        return jsonify({
            'message': 'Student does\'t exist'
        })

@app.route('/students/<int:id>', methods=['PUT', 'PATCH'])
def update_student(id):
    if request.method == 'PUT':
        name = request.form.get('name', None)
        surname = request.form.get('surname', None)
        program = request.form.get('program', None)
        
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
        })


@app.route('/students/<int:id>', methods=['DELETE'])
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
        })