from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUseManager
import uuid

# Create your models here.


class Department(models.Model):

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=220)
    description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [

        ('MANAGER','MANAGER'),
        ('EMPLOYEE','EMPLOYEE'),
    ]

    first_name = models.CharField(max_length=220)
    middle_name = models.CharField(max_length=220, blank=True,null=True)
    last_name = models.CharField(max_length=220)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True,blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default='EMPLOYEE')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUseManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email
