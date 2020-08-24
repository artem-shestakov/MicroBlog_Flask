import unittest
from webapp import create_app, db
from webapp.api import rest_api


class TestURL(unittest.TestCase):

    def setUp(self):
        rest_api.resources = []

        app = create_app("config.TestConfig")
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        db.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def test_root_url(self):
        """Test root URL"""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_post_redirect(self):
        """test redirect from /post to /"""
        result = self.client.get("/post")
        self.assertEqual(result.status_code, 308)


if __name__ == '__main__':
    unittest.main()
