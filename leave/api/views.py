from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from leave.api.serializers import EmployeeLeaveRequestSerializer
from leave.models import LeaveRequest
from .permissions import IsEmployee,IsLeaveRequestOwner


class EmployeeLeaveRequestViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeeLeaveRequestSerializer
    permission_classes = [IsEmployee, IsLeaveRequestOwner]
    lookup_field = "public_id"

    def get_queryset(self):
        return LeaveRequest.objects.filter(submitted_by=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        return serializer.save(submitted_by=self.request.user)


    def perform_update(self, serializer):
        leave_request = self.get_object()

        if leave_request.status != "PENDING":
            raise ValidationError("Approved or Rejected leave request cannot be modified.")

        serializer.save()

    def perform_destroy(self, instance):

        if instance.status != "PENDING":
            raise ValidationError("Approved or Rejected leave request cannot be deleted.")

        instance.is_deleted = True
        instance.save()
