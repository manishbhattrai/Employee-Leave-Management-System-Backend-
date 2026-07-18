from rest_framework import serializers
from  django.utils import timezone
from leave.models import LeaveRequest
from django.contrib.auth import get_user_model

User = get_user_model()

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

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError("End date cannot be before start date.")

        return data

class EmployeeNestedSerializer(serializers.ModelSerializer):

    department = serializers.CharField(source='department.name', read_only=True)
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','email','name','department']

    def get_name(self,obj):

        if obj.middle_name:
            return f"{obj.first_name} {obj.middle_name} {obj.last_name}"
        return f"{obj.first_name} {obj.last_name}"



class ManagerLeaveRequestSerializer(serializers.ModelSerializer):

    submitted_by = EmployeeNestedSerializer(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = ['public_id','submitted_by','reason',
                  'start_date','end_date','leave_type','status','created_at']
