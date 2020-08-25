import unittest
from webapp import create_app, db
from webapp.auth.models import Role, User
import json

class TestURL(unittest.TestCase):

    def setUp(self):
        app = create_app("config.TestConfig")
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        db.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()

    def _insert_user(self, email, f_name, password, role):
        test_role = Role(role)
        db.session.add(test_role)
        db.session.commit()

        test_user = User(email=email, f_name=f_name)
        test_user.set_password(password)
        db.session.add(test_user)
        db.session.commit()

    def test_root_url(self):
        """Test root URL"""

        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)

    def test_post_redirect(self):
        """test redirect from /post to /"""

        result = self.client.get("/post")
        self.assertEqual(result.status_code, 308)

    def test_login(self):
        """Test correct login and logout"""

        self._insert_user("test01@test.com", "test_user", "test", "user")
        result = self.client.post("auth/login", data=dict(
            email="test01@test.com",
            password="test"
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have been logged successfully", result.data.decode("utf-8"))

        result = self.client.get("auth/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have been logged out", result.data.decode("utf-8"))

    def test_fail_login(self):
        """Test fail login"""

        self._insert_user("test02@test.com", "test_user", "test", "user")
        result = self.client.post("auth/login", data=dict(
            email="test02@test.com",
            password="blabla"
        ), follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn("Invalid email or password", result.data.decode("utf-8"))

        result = self.client.get("post/new")
        self.assertEqual(result.status_code, 302)

    def test_unauthorized_access_to_admin(self):
        """Test access to admin panel by user role"""

        self._insert_user("test03@test.com", "test_user", "test", "user")
        result = self.client.post("auth/login", data=dict(
            email="test03@test.com",
            password="test"
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have been logged successfully", result.data.decode("utf-8"))

        result = self.client.get("admin/user/")
        self.assertEqual(result.status_code, 403)

    def test_api_jwt_login(self):
        """Test API JWT login"""

        self._insert_user("test01@test.com", "test_user", "test", "user")
        headers = {
            "Content-type": "application/json"
        }
        payload = {"email": "test01@test.com", "password": "test"}
        result = self.client.post("/auth/api", data=json.dumps(payload), headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_api_fail_jwt_login(self):
        """Test API JWT fail login"""
        headers = {
            "Content-type": "application/json"
        }
        self._insert_user("test01@test.com", "test_user", "test", "user")
        payload = {"email": "test01@test.com", "password": "blabla"}
        result = self.client.post("/auth/api", data=json.dumps(payload), headers=headers)

        self.assertEqual(result.status_code, 401)

    def test_api_new_post(self):
        """Test API add new post"""

        self._insert_user("test01@test.com", "test_user", "test", "user")
        headers = {
            "Content-type": "application/json"
        }
        payload = {"email": "test01@test.com", "password": "test"}
        result = self.client.post("/auth/api", data=json.dumps(payload), headers=headers)
        access_token = json.loads(result.data.decode("utf-8"))["access_token"]

        headers["Authorization"] = f"Bearer {access_token}"
        payload = {"title": "TestPost", "text": "TestText"}
        result = self.client.post("/api/post", data=json.dumps(payload), headers=headers)

        self.assertEqual(result.status_code, 201)


if __name__ == '__main__':
    unittest.main()
