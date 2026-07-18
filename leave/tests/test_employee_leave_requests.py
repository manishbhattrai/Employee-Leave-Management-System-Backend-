from datetime import timedelta, date
from .test_setup import TestSetup
from leave.models import LeaveRequest
from django.urls import reverse

class TestEmployeeLeaveRequestViewSet(TestSetup):

    def test_employee_can_create_leave_request(self):
        self.client.force_authenticate(self.employee)

        payload = {

            "reason":"Sick Leave",
            "start_date":"2026-07-18",
            "end_date":"2026-07-20",
            "leave_type":"SICK",
        }

        response = self.client.post(
            self.employee_leave_request_list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code,201)

        leave = LeaveRequest.objects.get(reason="Sick Leave")
        self.assertEqual(leave.status, "PENDING")

    def test_employee_cannot_create_leave_without_reason(self):
        self.client.force_authenticate(self.employee)
        payload = {
            "start_date": "2026-07-20",
            "end_date": "2026-07-22",
            "leave_type":"PAID"
        }

        response = self.client.post(
            self.employee_leave_request_list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("reason",response.data)

    def test_employee_cannot_create_leave_without_dates(self):
        self.client.force_authenticate(self.employee)

        payload = {
            "reason": "Personal work",
            "leave_type":"CASUAL"
        }

        response = self.client.post(
            self.employee_leave_request_list_url,
            payload,
            format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_end_date_cannot_be_before_start_date(self):
        self.client.force_authenticate(self.employee)

        payload = {
            "reason": "Sick Leave",
            "start_date": "2026-07-25",
            "end_date": "2026-07-20",
            "leave_type":"SICK"
        }

        response = self.client.post(
            self.employee_leave_request_list_url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_user_cannot_create_leave(self):

        payload = {

            "reason": "Sick Leave",
            "start_date": "2026-07-18",
            "end_date": "2026-07-20",
            "leave_type": "SICK",
        }

        response = self.client.post(
            self.employee_leave_request_list_url,
            payload,
            format='json'
        )

        self.assertEqual(response.status_code, 401)

    def test_employee_can_list_leave_requests(self):
        self.client.force_authenticate(self.employee)

        response = self.client.get(
            self.employee_leave_request_list_url
        )

        self.assertEqual(response.status_code, 200)

    def test_employee_cannot_access_other_employee_leave(self):
        self.client.force_authenticate(self.employee)

        leave = LeaveRequest.objects.create(
            submitted_by=self.other_employee,
            reason="Other leave",
            start_date="2026-07-20",
            end_date="2026-07-22",
            leave_type="CASUAL"
        )

        url = reverse("employee-leave-request-detail",kwargs={"public_id": leave.public_id} )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_employee_can_update_pending_leave(self):
        self.client.force_authenticate(self.employee)

        url = reverse("employee-leave-request-detail",kwargs={"public_id": self.leave_request.public_id})
        payload = {
            "reason":"Updated reason"
        }

        response = self.client.patch(
            url,
            payload,
            format="json"
        )
        self.assertEqual(response.status_code, 200)

    def test_employee_cannot_update_approved_leave(self):
        self.client.force_authenticate(self.employee)

        self.leave_request.status = "APPROVED"
        self.leave_request.save()

        url = reverse("employee-leave-request-detail",kwargs={"public_id": self.leave_request.public_id})
        payload = {
                "reason": "Changed reason"
        }

        response = self.client.patch(
            url,
            payload,
            format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_employee_cannot_update_rejected_leave(self):
        self.client.force_authenticate(self.employee)

        self.leave_request.status = "REJECTED"
        self.leave_request.save()

        url = reverse("employee-leave-request-detail", kwargs={"public_id": self.leave_request.public_id})
        payload = {
            "reason": "Changed reason"
        }

        response = self.client.patch(
            url,
            payload,
            format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_employee_cannot_delete_approved_leave(self):
        self.client.force_authenticate(self.employee)

        self.leave_request.status = "APPROVED"
        self.leave_request.save()

        url = reverse("employee-leave-request-detail", kwargs={"public_id": self.leave_request.public_id})

        response = self.client.delete(
            url,
        )
        self.assertEqual(response.status_code, 400)

    def test_employee_cannot_delete_rejected_leave(self):
        self.client.force_authenticate(self.employee)

        self.leave_request.status = "APPROVED"
        self.leave_request.save()

        url = reverse("employee-leave-request-detail", kwargs={"public_id": self.leave_request.public_id})

        response = self.client.delete(
            url,
        )
        self.assertEqual(response.status_code, 400)

    def test_leave_request_pagination(self):
        self.client.force_authenticate(self.employee)

        for i in range(15):
            LeaveRequest.objects.create(
                submitted_by=self.employee,
                reason="other leave",
                leave_type="PAID",
                status="PENDING",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=3)
            )

        response = self.client.get(
            self.employee_leave_request_list_url
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(response.data["count"], 16)
        self.assertIsNotNone(response.data["next"])

    def test_filter_leave_requests_by_status(self):
        self.client.force_authenticate(user=self.employee)

        LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="PAID",
            reason="other leave",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3)
        )

        LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="CASUAL",
            reason= "other leave",
            status="APPROVED",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3)
        )

        url = reverse("employee-leave-request-list") + "?status=APPROVED"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_leave_requests_by_leave_type(self):
        self.client.force_authenticate(user=self.employee)

        LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="PAID",
            reason="other leave",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3)
        )

        LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="CASUAL",
            reason="other leave",
            status="APPROVED",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3)
        )

        url = reverse("employee-leave-request-list") + "?leave_type=PAID"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_filter_leave_requests_by_status_and_leave_type(self):
        self.client.force_authenticate(user=self.employee)

        LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="PAID",
            reason="other leave",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3)
        )

        LeaveRequest.objects.create(
            submitted_by=self.employee,
            leave_type="CASUAL",
            reason="other leave",
            status="APPROVED",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=3)
        )

        url = reverse("employee-leave-request-list") + "?status=APPROVED&leave_type=CASUAL"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)