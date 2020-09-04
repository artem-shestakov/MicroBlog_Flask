import unittest
from webapp import create_app, db
from webapp.auth.models import Role, User
import json
from flask import current_app


class TestURL(unittest.TestCase):

    def setUp(self):
        """
        Create temp application and database in memory for tests
        """
        app = create_app("config.TestConfig")
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        db.app = app
        db.create_all()
        self.app = app

    def tearDown(self):
        """Close connection to database"""

        db.session.remove()

    def _insert_user(self, email, f_name, password, role):
        """ Create role and user

        :param email: User's email
        :param f_name: User's first name
        :param password: User's account password
        :param role: User's blog role
        """

        with self.app.app_context():
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

    def test_login_logout(self):
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
        # Test incorrect password
        payload = {"email": "test01@test.com", "password": "blabla"}
        result = self.client.post("/auth/api", data=json.dumps(payload), headers=headers)
        self.assertEqual(result.status_code, 401)

        # Test missing arguments
        payload = {"email": "test01@test.com"}
        result = self.client.post("/auth/api", data=json.dumps(payload), headers=headers)
        self.assertEqual(result.status_code, 400)

        payload = {"password": "test"}
        result = self.client.post("/auth/api", data=json.dumps(payload), headers=headers)
        self.assertEqual(result.status_code, 400)

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

    def test_email_confirmation(self):
        """Test user's email confirmation process"""
        # Add user
        self._insert_user("test01@test.com", "test_user", "test", "user")

        # Get email status
        user = User.query.filter_by(email="test01@test.com").first_or_404()
        self.assertEqual(user.email_confirm, False)

        # Create token for email confirmation
        from webapp.auth.utils import generate_confirm_token
        with self.app.app_context():
            token = generate_confirm_token("test01@test.com")

        # GET email confirmation
        result = self.client.get(f"/auth/email-confirm/{token}")
        self.assertEqual(result.status_code, 302)

        # GET root address with answer from URL '/auth/email-confirm/'
        result = self.client.get("/")
        self.assertIn("You have confirmed your account!", result.data.decode("utf-8"))

        # Check /unconfirmed URL
        result = self.client.get("/auth/unconfirmed")
        self.assertEqual(result.status_code, 302)

    def test_fail_email_confirmation(self):
        """Test fail user's email confirmation process with not valid token"""
        # Add user
        self._insert_user("test01@test.com", "test_user", "test", "user")

        # Request with not valid token
        result = self.client.get(f"/auth/email-confirm/{b'abc.abc'}")
        self.assertEqual(result.status_code, 302)

        # Get root address with answer from URL '/auth/email-confirm/'
        result = self.client.get("/")
        self.assertIn("The confirm link invalid", result.data.decode("utf-8"))

        result = self.client.post("auth/login", data=dict(
            email="test01@test.com",
            password="test"
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have been logged successfully", result.data.decode("utf-8"))

        # Check /unconfirmed URL
        result = self.client.get("/auth/unconfirmed")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Please confirm your email", result.data.decode("utf-8"))

    def test_password_reset(self):
        """Test reset user's password"""
        # Add user
        self._insert_user("test01@test.com", "test_user", "test", "user")

        # Check /forgot-password URL
        result = self.client.post("/auth/forgot-password", data=dict(
            email="test01@test.com"
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)

        # Reset password
        from webapp.auth.utils import generate_reset_pass_token
        with self.app.app_context():
            token = generate_reset_pass_token("test01@test.com")
        result = self.client.post(f"/auth/reset-password/{token}", data=dict(
            password="new_pass",
            confirm_password="new_pass"
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)

        # Check login
        result = self.client.post("auth/login", data=dict(
            email="test01@test.com",
            password="new_pass"
        ), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("You have been logged successfully", result.data.decode("utf-8"))


if __name__ == '__main__':
    unittest.main()
