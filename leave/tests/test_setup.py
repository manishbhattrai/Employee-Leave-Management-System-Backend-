from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from leave.models import LeaveRequest
from users.models import Department

User = get_user_model()


class TestSetup(APITestCase):

    def setUp(self):

        self.employee_leave_request_list_url = reverse("employee-leave-request-list")
        self.manager_leave_request_list_url = reverse("manager-leave-request-list")

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

        self.other_employee = User.objects.create_user(

            email="otheremployee@gmail.com",
            password="otherpassword123",
            first_name="john",
            last_name="doe",
            role="EMPLOYEE",
            department=self.department
        )

        self.manager = User.objects.create_user(

            email="manager@gmail.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            role="MANAGER",
            department=self.department,

        )

        self.leave_request = LeaveRequest.objects.create(

            submitted_by=self.employee,
            reason="Medical leave",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            status="PENDING",
            leave_type="SICK"
        )

        self.client = APIClient()