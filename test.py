from flask_testing import TestCase
from app import app, db
import unittest
import os
import sqlalchemy
import testscenarios

load_tests = testscenarios.load_tests_apply_scenarios

class FlaskTestCase(unittest.TestCase):
    scenarios = [('mysql', dict(database_connection=os.getenv("MYSQL_TEST_URL")))]
    
    # def setUp(self):
    #    if not self.database_connection:
    #        self.skipTest("No database URL set")
    #    self.engine = sqlalchemy.create_engine(self.database_connection)
    #    self.connection = self.engine.connect()
    #    self.connection.execute("CREATE DATABASE testdb")

    # def tearDown(self):
    #     self.connection.execute("DROP DATABASE testdb")

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
    
    def register(self, email, username, pswrd, cfpw):
        tester = app.test_client(self)
        return tester.post('/signup', data=dict(email=email, username=username, pswrd=pswrd, cfpw=cfpw),follow_redirects=True)
    
    def login(self, username, pswrd):
        tester = app.test_client(self)
        return tester, tester.post('/', data=dict(username=username, pswrd=pswrd), follow_redirects=True)

    def test_login_valid(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/threads', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Home' in response.data)

    def test_login_invalid(self):
        tester, response = self.login('admin', '1234567')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/threads', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Welcome to MoneyLine<br>Log In' in response.data)
    
    def test_signup_valid(self):
        response = self.register('testEmail@gmail.com', 'signupTester', '12345', '12345')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Thank you for registering. Welcome to MoneyLine!", response.data)

    def test_signup_invalid_different_pw(self):
        response = self.register('testEmail2@gmail.com', 'signUpTester2', '12345', '12345678') 
        self.assertIn(b"Invalid password!", response.data)

    def test_signup_invalid_duplicate_username(self):
        response = self.register('testEmail3@gmail.com', 'signupTester3', '12345', '12345')
        self.assertEqual(response.status_code, 200)
        response = self.register('testEmail4@gmail.com', 'signupTester3', '12345679', '12345679')
        self.assertIn(b"Username already exists!", response.data)
    
    def test_signup_invalid_duplicate_email(self):
        response = self.register('testEmail5@gmail.com', 'signupTester5', '12345', '12345')
        self.assertEqual(response.status_code, 200)
        response = self.register('testEmail5@gmail.com', 'signUpTester6', '123456', '123456')
        # self.assertIn(b"Invalid email address!", response.data)
        self.assertEqual(response.status_code, 200)

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
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/newPost', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Welcome to MoneyLine<br>Log In' in response.data)

    def test_threads_loads(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/threads', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Home' in response.data)
    
    def test_thread_detail_loads(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/threads/7', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Thread' in response.data)
        self.assertTrue(b'testing1' in response.data)

    def test_games_loads(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/games', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Games' in response.data)


    def test_newPost_loads(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/newPost', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Add a post' in response.data)
        response = tester.get('/threads', follow_redirects=True)

    def test_faq_loads(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/faq', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Betting 101' in response.data)
        self.assertTrue(b'Betting FAQ' in response.data)

    def test_profile_loads(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Profile' in response.data)
    
    def test_edit_profile_load(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/edit_profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Edit Profile' in response.data)
        
    def test_mylist_load(self):
        tester, response = self.login('admin', '123456')
        self.assertEqual(response.status_code, 200)
        response = tester.get('/myList', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'My Betting List' in response.data)

if __name__ == '__main__':
    unittest.main()