from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from leave.api.serializers import EmployeeLeaveRequestSerializer, ManagerLeaveRequestSerializer
from leave.models import LeaveRequest
from .permissions import IsEmployee, IsLeaveRequestOwner, IsManager


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

class ManagerLeaveRequestViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ManagerLeaveRequestSerializer
    permission_classes = [IsManager]
    lookup_field = "public_id"

    def get_queryset(self):
        return (
            LeaveRequest.objects.select_related('submitted_by','submitted_by__department')
            .filter(is_deleted=False)
        )

    @action(detail=True, methods=["patch"])
    def approve(self, request, public_id=None):

        leave_request = self.get_object()

        if leave_request.status != "PENDING":
            return Response({"message":"Leave request has already been processed."},
                            status=status.HTTP_400_BAD_REQUEST
            )
        leave_request.status = "APPROVED"
        leave_request.save()

        return Response({"message":"Leave request approved."},
                        status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["patch"])
    def reject(self, request, public_id=None):

        leave_request = self.get_object()

        if leave_request.status != "PENDING":
            return Response({"message":"Leave request has already been processed."},
                            status=status.HTTP_400_BAD_REQUEST
            )
        leave_request.status = "REJECTED"
        leave_request.save()

        return Response({"message":"Leave request rejected."},
                        status=status.HTTP_200_OK
        )