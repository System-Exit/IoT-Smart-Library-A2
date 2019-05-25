import unittest
from voice_ui import VoiceRecognition

class TestVoiceRecognition(unittest.TestCase):
    
    def test_voice_search_book(self):
        self.assertEqual('test'.search_books(), '1|Test1|TestAuthor| 2019-05-14')
