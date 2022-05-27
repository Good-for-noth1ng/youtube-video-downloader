import unittest
from django.test import TestCase
from tgbot.handlers.download_handler.handler import check_youtube_domain

class URLTest(unittest.TestCase):

    def test_check_youtube_domain(self):
        result = check_youtube_domain('youtube.com')
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()
