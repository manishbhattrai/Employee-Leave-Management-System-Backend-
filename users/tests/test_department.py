from .test_setup import TestSetup
from django.urls import reverse
from users.models import Department


class TestDepartment(TestSetup):

    def test_superuser_can_create_department(self):
        self.client.force_authenticate(self.superuser)

        payload = {
            "name": "Engineering"
        }

        response = self.client.post(
            self.department_create_list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Department.objects.filter(name="Engineering").exists())


    def test_managers_can_create_department(self):
        self.client.force_authenticate(self.superuser)

        payload = {
            "name":"Finance"
        }
        response = self.client.post(
            self.department_create_list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Department.objects.filter(name="Finance").exists())


    def test_employee_cannot_create_department(self):
        self.client.force_authenticate(self.employee)

        payload = {
            "name": "HR"
        }
        response = self.client.post(
            self.department_create_list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Department.objects.filter(name="HR").exists())

    def test_retrieve_department_using_public_id(self):
        self.client.force_authenticate(self.manager)

        url = reverse("department-detail",kwargs={"public_id": self.department.public_id})

        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data["name"],"IT")

    def test_invalid_public_id_returns_404(self):
        self.client.force_authenticate(self.manager)

        url = reverse("department-detail", kwargs={"public_id":"invalid_id"})

        response = self.client.get(
            url
        )
        self.assertEqual(response.status_code, 404)

    def test_manager_can_update_department(self):
        self.client.force_authenticate(self.manager)

        department = Department.objects.create(
            name="Health"
        )

        url = reverse("department-detail",kwargs={ "public_id": department.public_id})

        payload = {
            "name": "Updated Department"
        }

        response = self.client.patch(
            url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_cannot_update_department(self):
        self.client.force_authenticate(self.employee)

        url = reverse("department-detail",kwargs={"public_id": self.department.public_id})

        payload = {
            "name": "New Name"
        }
        response = self.client.patch(
            url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code,403)

    def test_manager_can_delete_department(self):
        self.client.force_authenticate(self.manager)

        department = Department.objects.create(
            name="test department"
        )

        url = reverse("department-detail", kwargs={"public_id": department.public_id})

        response = self.client.delete(
            url,
        )

        self.assertEqual(response.status_code, 204)


    def test_employee_cannot_delete_department(self):
        self.client.force_authenticate(self.employee)

        url = reverse("department-detail", kwargs={"public_id":self.department.id})
        response = self.client.delete(
            url
        )

        self.assertEqual(response.status_code, 403)

    def test_employee_can_see_list_departments(self):
        self.client.force_authenticate(self.employee)

        response = self.client.get(
           self.department_create_list_url
        )
        self.assertEqual(response.status_code, 200)