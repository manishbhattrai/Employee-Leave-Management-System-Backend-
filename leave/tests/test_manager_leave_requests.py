from .test_setup import TestSetup
from leave.models import LeaveRequest
from django.urls import reverse
from datetime import date, timedelta


class TestManagerLeaveRequestViewSet(TestSetup):

    def test_manager_can_view_all_leave_requests(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.get(
            self.manager_leave_request_list_url
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], LeaveRequest.objects.count())

    def test_manager_can_view_leave_request_detail(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse("manager-leave-request-detail", kwargs={"public_id":self.leave_request.public_id})
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["public_id"], str(self.leave_request.public_id))

    def test_manager_can_filter_by_leave_type(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse("manager-leave-request-list")+ "?leave_type=SICK"
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code,200)

        for leave in response.data["results"]:
            self.assertEqual(leave["leave_type"], "SICK")

    def test_manager_can_filter_by_status(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse("manager-leave-request-list") + "?status=PENDING"
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code, 200)

        for leave in response.data["results"]:
            self.assertEqual(leave["status"], "PENDING")

    def test_manager_can_search_by_first_name(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse("manager-leave-request-list") + "?search=john"
        response = self.client.get(
           url
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_manager_can_search_by_last_name(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse("manager-leave-request-list") + "?search=doe"
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_manager_search_no_results(self):
        self.client.force_authenticate(user=self.manager)

        url = reverse("manager-leave-request-list") + "?search=UnknownPerson"
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_employee_cannot_search_manager_leave_requests(self):
        self.client.force_authenticate(user=self.employee)

        url = reverse("manager-leave-request-list") + "?search=John"
        response = self.client.get(
            url
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_leave_request_pagination(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.get(
            self.manager_leave_request_list_url
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)

    def test_employee_cannot_access_manager_leave_requests(self):
        self.client.force_authenticate(user=self.employee)

        response = self.client.get(
            self.manager_leave_request_list_url
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_approve_leave(self):
        self.client.force_authenticate(user=self.manager)

        leave_request = LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="SICK",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
            reason="Medical leave",
        )

        url = reverse("manager-leave-request-approve", kwargs={"public_id":leave_request.public_id})

        response = self.client.patch(
            url
        )

        self.assertEqual(response.status_code, 200)

        leave_request.refresh_from_db()
        self.assertEqual(leave_request.status, "APPROVED")

    def test_manager_cannot_approve_processed_leave(self):
        self.client.force_authenticate(user=self.manager)

        leave_request = LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="SICK",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
            reason="Medical leave",
            status="APPROVED"
        )

        url = reverse("manager-leave-request-approve",kwargs={"public_id": leave_request.public_id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.data["message"],"Leave request has already been processed.")


    def test_manager_can_reject_leave(self):
        self.client.force_authenticate(user=self.manager)

        leave_request = LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="SICK",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
            reason="Medical leave",
        )

        url = reverse("manager-leave-request-reject", kwargs={"public_id": leave_request.public_id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 200)

        leave_request.refresh_from_db()
        self.assertEqual(leave_request.status, "REJECTED")


    def test_manager_cannot_reject_processed_leave(self):
        self.client.force_authenticate(self.manager)

        leave_request = LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="SICK",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3),
            reason="Medical leave",
            status="REJECTED"
        )
        url = reverse("manager-leave-request-reject", kwargs={"public_id": leave_request.public_id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Leave request has already been processed.")

