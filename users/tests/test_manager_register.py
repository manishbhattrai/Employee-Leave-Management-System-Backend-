from .test_setup import TestSetup
from django.contrib.auth import get_user_model

User = get_user_model()

class TestManagerRegister(TestSetup):


    def test_superuser_can_create_manager(self):
        self.client.force_authenticate(self.superuser)

        payload = {
            "email":"testmanager@gmail.com",
            "password":"password@123",
            "confirm_password": "password@123",
            "first_name":"john",
            "last_name":"doe",
            "role":"MANAGER",
        }

        response = self.client.post(
            self.manager_register_url,
            payload,
            format='json'
        )

        self.assertEqual(response.status_code,201)
        self.assertEqual(User.objects.count(), 4)

        manager = User.objects.get(email="testmanager@gmail.com")
        self.assertEqual(manager.role, "MANAGER")

    def test_employee_cannot_create_manager(self):
        self.client.force_authenticate(self.employee)

        payload = {
            "email": "testmanager2@gmail.com",
            "password": "password123",
            "confirm_password":"password123",
            "first_name": "John",
            "last_name": "Doe",
            "role": "MANAGER",
        }

        response = self.client.post(
            self.manager_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(
            User.objects.filter(email="testmanager2@gmail.com").exists()
        )

    def test_manager_cannot_create_manager(self):
        self.client.force_authenticate(self.manager)

        payload = {
            "email": "testmanager3@gmail.com",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "role": "MANAGER",
        }

        response = self.client.post(
            self.manager_register_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 403)

        self.assertFalse(
            User.objects.filter(email="testmanager3@gmail.com").exists()
        )
