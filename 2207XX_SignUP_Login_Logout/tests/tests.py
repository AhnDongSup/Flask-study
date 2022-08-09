import unittest
from os import path

from flask_login import current_user
from bs4 import BeautifulSoup

from blog import create_app
from blog import db
import os

from blog.models import User, get_user_model

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
app.testing = True

class TestAuth(unittest.TestCase):
    
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        
        self.db_uri = 'sqlite:///'+os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
        if not path.exists("tests/" + "test_db"):
            db.create_all(app=app)
        db.session.close()
        db.engine.dispose()
        
    def tearDown(self):
        os.unlink('tests/test.db')
        self.ctx.pop()
    
    def test_signup_by_datebase(self):
   
        self.user_test_1 = get_user_model()(
            email = "ExEmail@test.com",
            username = "testname",
            password="test1234",
            is_staff=True
        )
        db.session.add(self.user_test_1)
        db.session.commit()
        
        self.user_test_2 =get_user_model()(
            email = "ExEx@test.com",
            username = "test2",
            password = "test1234"
        )
        db.session.add(self.user_test_2)
        db.session.commit()
        
        self.assertEqual(get_user_model().query.count(), 2)
        
        db.session.close()
        db.engine.dispose()
        

    def test_signup_by_form(self):
        response = self.client.post('/auth/sign-up', data=dict(email="EEmail@test.com", username="testsname",password1="test1234",password2="test1234"))
        print("===",response.status_code,"===")
        self.assertEqual(get_user_model().query.count(), 1)
        db.session.close()
        db.engine.dispose()
        