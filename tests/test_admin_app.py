import admin_app
import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self):
        admin_app.app.testing = True
        self.app = admin_app.app.test_client()
    
    def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])

    def test_home(self):
        result = self.app.get('/')
        # Make your assertions
    
    def test_login(self):

    def test_input(self):

    