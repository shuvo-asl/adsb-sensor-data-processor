import unittest
from app import app

class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config.update({
            "TESTING": True
        })
        self.app = app.test_client()

    def tearDown(self) -> None:
        pass