from .test_setup import TestSetup
from django.contrib.auth import get_user_model

User = get_user_model()


class TestEmployeeRegister(TestSetup):

    def test_employee_can_register(self):

        payload = {
            "email": "employee1@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John",
            "middle_name": "Michael",
            "last_name": "Doe",
            "department": self.department.id,
        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code,201)
        self.assertTrue(User.objects.filter(email="employee1@gmail.com").exists())

    def test_employee_cannot_register_with_existing_email(self):

        payload = {
            "email": self.employee.email,
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "department": self.department.id,
        }
        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_first_name_min_length_validation(self):

        payload = {
            "email": "employee2@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "Jo",
            "last_name": "Smith",
            "department": self.department.id,

        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.data)

    def test_first_name_only_letters(self):

        payload = {
            "email": "employee3@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John123",
            "last_name": "Smith",
            "department": self.department.id,
        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.data)

    def test_middle_name_only_letters(self):

        payload = {
            "email": "employee4@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John",
            "middle_name": "123",
            "last_name": "Smith",
            "department": self.department.id,
        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("middle_name", response.data)

    def test_last_name_only_letters(self):

        payload = {
            "email": "employee5@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John",
            "last_name": "Smith123",
            "department": self.department.id,
        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("last_name", response.data)

    def test_only_gmail_allowed(self):

        payload = {
            "email": "employee6@yahoo.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John",
            "last_name": "Smith",
            "department": self.department.id,
        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_password_confirmation_mismatch(self):

        payload = {
            "email": "employee7@gmail.com",
            "password": "password123",
            "confirm_password": "different123",
            "first_name": "John",
            "last_name": "Smith",
            "department": self.department.id,
        }

        response = self.client.post(
            self.employee_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)