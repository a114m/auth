import unittest
from flask_testing import TestCase
import json

from app import create_app
from models import db, User, Group, Resource


class GroupTest(TestCase):

    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.create_all()

    def test_create_group(self):
        response = self.client.post(
            "/group",
            data=json.dumps({"name": "group a"}),
            content_type="application-json"
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
