from .test_setup import TestSetup


class TestLogin(TestSetup):

    def test_user_can_login_with_valid_credentials(self):

        payload = {
            "email": "employee@gmail.com",
            "password": "password123",
        }

        response = self.client.post(
            self.login_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["message"],"login successful.")

    def test_login_fails_with_wrong_password(self):

        payload = {
            "email": "manager@gmail.com",
            "password": "wrongpassword",
        }

        response = self.client.post(
            self.login_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 401)

    def test_login_fails_for_unknown_user(self):

        payload = {
            "email": "unknown@gmail.com",
            "password": "password123",
        }

        response = self.client.post(
            self.login_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 401)