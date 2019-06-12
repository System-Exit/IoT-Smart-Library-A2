import unittest
import requests
from admin_app.app import app


class appTests(unittest.TestCase):

  def setUp(self):
    # create a test client
    self.app = app.test_client()
    
    self.app.testing = True
  
  def tearDown(self):
    pass
    
  def test_index_status_good_return_code(self):
    #Send a GET request to home page of app
    response = self.app.get('/')

    #Check is respinse is a 200 code
    self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()