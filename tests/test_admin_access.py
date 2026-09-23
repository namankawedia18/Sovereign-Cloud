import unittest

from app import app


class AdminAccessTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_admin_users_requires_login(self):
        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 302)

    def test_admin_policies_requires_login(self):
        response = self.client.get('/admin/policies')
        self.assertEqual(response.status_code, 302)

    def test_normal_user_can_access_upload_page(self):
        from models.user import User
        from extensions import db
        from werkzeug.security import generate_password_hash

        with app.app_context():
            user = User.query.filter_by(email='user@test.com').first()
            if not user:
                user = User(username='tester', email='user@test.com', password_hash=generate_password_hash('pass123'), role='user')
                db.session.add(user)
                db.session.commit()

            with self.client.session_transaction() as session:
                session['_user_id'] = str(user.id)
                session['_fresh'] = True

        response = self.client.get('/upload')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
