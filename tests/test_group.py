import unittest
from flask_testing import TestCase
import json

from models import db, Group


class GroupTest(TestCase):

    def create_app(self):
        return db.get_app()

    def setUp(self):
        db.create_all()

    def test_create_group(self):
        group = {"name": "group a"}
        response = self.client.post(
            "/group",
            data=json.dumps(group),
            content_type="application-json"
        )
        # test response status code
        self.assertEqual(response.status_code, 200)
        # test response body has the same group name of one in request
        self.assertDictContainsSubset(group, response.json)
        # get the group from DB to and compare to one in request to assure it's stored
        stored_group = db.session.query(Group).first()
        self.assertDictContainsSubset(group, stored_group.__dict__)

    def test_get_group(self):
        group = {
            "name": "groupie",
            "description": "groupie desc"
        }
        group_orm = Group(**group)
        db.session.add(group_orm)
        db.session.commit()

        response = self.client.get(
            "/group/%s" % group_orm.id,
            content_type="application-json"
        )
        # test response status code
        self.assertEqual(response.status_code, 200)
        # test the response name, desc are the same as ones stored in DB
        self.assertDictContainsSubset(group, response.json)
        # test the response group has id
        self.assertIn("id", response.json)

    def test_list_group(self):
        # fixtures
        groups = [
            {
                "name": "groupie_a",
                "description": "groupie_a desc"
            },
            {
                "name": "groupie_b",
                "description": "groupie_b desc"
            },
            {
                "name": "groupie_c",
                "description": "groupie_c desc"
            }
        ]

        groups_orm = list()
        for group in groups:
            group_orm = Group(**group)
            db.session.add(group_orm)
            groups_orm.append(group_orm)
        db.session.commit()

        # adding returned ids from DB to the fixtures to compare them later ro response
        groups = list(map(lambda i: dict(groups[i], id=groups_orm[i].id), range(len(groups))))

        response = self.client.get(
            "/group",
            content_type="application-json"
        )
        # test response status code
        self.assertEqual(response.status_code, 200)
        # test response count value
        self.assertEqual(response.json['count'], 3)
        # test response actual returned objects count
        self.assertEqual(len(response.json['items']), 3)
        # checking if each of the fixtures are included in the items (doing it this way instead of direct compare because order isn't always guaranteed)
        self.assertTrue(all(map(lambda group: group in response.json['items'], groups)))

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
