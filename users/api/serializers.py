from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Department

User = get_user_model()

class EmployeeRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name',
                  'email','department','password','confirm_password']


    def validate_first_name(self, value):

        if len(value) < 3:
            raise serializers.ValidationError("Frist Name should be more than 2 characters.")

        if not value.isalpha():
            raise serializers.ValidationError("First Name should contain only letters.")

        return value.lower()

    def validate_middle_name(self,value):

        if not value.isalpha():
            raise serializers.ValidationError("Middle Name should contain only letters.")

        return value.lower()

    def validate_last_name(self,value):

        if not value.isalpha():
            raise serializers.ValidationError("Last Name should contain only letters.")

        return value.lower()

    def validate_email(self,value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")

        return value.lower()

    def validate(self,data):

        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Password didn't match.")

        return data


    def create(self, validated_data):

        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['public_id','name','description','created_at','updated_at']
        read_only_fields = ['public_id','created_at','updated_at']