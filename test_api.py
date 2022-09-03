from os import unlink
import unittest
from app import app
from flask_sqlalchemy import SQLAlchemy
import json


class ApiTest(unittest.TestCase):
    
    # Setup
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.app.config.from_object('config') 
        
        with self.app.app_context():
            db = SQLAlchemy()
            db.init_app(self.app)
            db.create_all()

    def tearDown(self):
        pass
    
    
    # fonctions test_nom_de_fonction
    def test_list_students(self):
        response = self.client().get('/api/students')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['students'])
    
    def test_get_etudiant(self):
        response = self.client().get('/api/students/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()
