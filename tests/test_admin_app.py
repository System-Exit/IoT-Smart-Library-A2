import admin_app
import unittest


class AdminAppTestCase(unittest.TestCase):

    def setUp(self):
        
        # change database to cloud 
        self.db_fd, admin_app.app.config['DATABASE'] = tempfile.mkstemp()
        admin_app.app.testing = True
        self.app = admin_app.app.test_client()

        with admin_app.app.app_context():
            admin_app.init_db()

    def tearDown(self):
        
        os.close(self.db_fd)
        os.unlink(admin_app.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_home(self):
        result = self.app.get('/')
        # Make your assertions
    
    def login(self, username, password):
    return self.app.post('/login', data=dict( username=username, password=password), follow_redirects=True)

    def logout(self):
    return self.app.get('/logout', follow_redirects=True)
    
if __name__ == '__main__':
    unittest.main()

    