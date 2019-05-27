import admin_app
import unittest


class AdminAppTestCase(unittest.TestCase):

    def setUp(self):
        
        self.db_fd, admin_app.app.config['DATABASE'] = tempfile.mkstemp()
        admin_app.app.testing = True
        self.app = admin_app.app.test_client()

        with admin_app.app.app_context():
            admin_app.init_db()

    def tearDown(self):
        
        os.close(self.db_fd)
        os.unlink(admin_app.app.config['DATABASE'])

    def test_home(self):
        result = self.app.get('/')
        # Make your assertions
    
    def test_login(self):

    def test_input(self):

    