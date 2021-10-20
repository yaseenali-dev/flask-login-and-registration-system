import unittest
from app.models import User

#  not in a mood to write more test

class TestUserModel(unittest.TestCase):
    def test_verify_password(self):
        u = User(email='james@j.com', password='secret')
        self.assertTrue(u.verify_password('secret'))

    def test_random_salt(self):
        u = User(email='james@j.com', password='secret')
        u1 = User(email='jack@j.com', password='321')
        self.assertNotEqual(u.password_hash, u1.password_hash)

    def test_password_setter(self):
        u = User(email='james@j.com', password='secret')
        self.assertTrue(u.password_hash is not None)

    def test_password_attribute_error(self):
        u = User(email='james@j.com', password='secret')
        with self.assertRaises(AttributeError):
            u.password
