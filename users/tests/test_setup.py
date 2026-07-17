from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Department

User = get_user_model()


class TestSetup(APITestCase):

    def setUp(self):

        self.login_url = reverse('login')
        self.employee_register_url = reverse('register-employee')
        self.manager_register_url = reverse('create-manager')
        self.department_create_list_url = reverse('department-list')

        self.department = Department.objects.create(
            name="IT",
        )

        self.superuser = User.objects.create_superuser(

            email = "testadmin@gmail.com",
            password = "testpassword@123",
        )

        self.employee = User.objects.create_user(

            email="employee@gmail.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            role="EMPLOYEE",
            department=self.department,
        )

        self.manager = User.objects.create_user(

            email="manager@gmail.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            role="MANAGER",
            department=self.department,

        )

        self.client = APIClient()