from rest_framework import serializers
from  django.utils import timezone
from leave.models import LeaveRequest

class EmployeeLeaveRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        fields = ['public_id','reason','start_date',
                  'end_date','status','leave_type','created_at']

        read_only_fields = ['public_id','status','created_at']

    def validate_start_date(self,value):

        if value < timezone.now().date():
            raise serializers.ValidationError("Cannot apply leave request for past date.")

        return value

    def validate(self,data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")

        return data