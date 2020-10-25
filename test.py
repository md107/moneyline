from flask_testing import TestCase
from app import app, db
import unittest

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        self.assertEqual(app.debug, False)
 
    def tearDown(self):
        pass

    # Ensure that login page load correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')        
        self.assertEqual(response.status_code, 200)

    def test_login_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Welcome to MoneyLine<br>Log In' in response.data)
    
    def test_about(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_signup_loads(self):
        tester = app.test_client(self)
        response = tester.get('/signup', follow_redirects=True)
        self.assertTrue(b'Sign Up' in response.data)
    
    def test_forgotpw_loads(self):
        tester = app.test_client(self)
        response = tester.get('/reset_pw', content_type='html/text')
        self.assertTrue(b'Forgot Password' in response.data)
    
    def test_incorrect_credentials(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username='longp19', password='aaa'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_correct_credentials(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username='longp19', password='longp19'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/', data=dict(username='longp19', password='longp19'), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_threads_loads(self):
        tester = app.test_client(self)
        response = tester.get('/threads', follow_redirects=True)
        self.assertTrue(b'Home' in response.data)

    def test_games_loads(self):
        tester = app.test_client(self)
        response = tester.get('/games', follow_redirects=True)
        self.assertTrue(b'Games' in response.data)

    def test_newPost_loads(self):
        tester = app.test_client(self)
        response = tester.get('/newPost', follow_redirects=True)
        self.assertTrue(b'Add a post' in response.data)

    def test_faq_loads(self):
        tester = app.test_client(self)
        response = tester.get('/faq', follow_redirects=True)
        self.assertTrue(b'Betting 101' in response.data)
        self.assertTrue(b'Betting FAQ' in response.data)

    def test_profile_loads(self):
        tester = app.test_client(self)
        response = tester.get('/profile', follow_redirects=True)
        print(response.data)
        self.assertTrue(b'Profile' in response.data)
    

if __name__ == '__main__':
    unittest.main()