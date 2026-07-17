import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class LeaveRequest(models.Model):

    LEAVE_TYPE_CHOICES = [
        ('SICK','SICK'),
        ('CASUAL','CASUAL'),
        ('PAID','PAID'),
    ]

    STATUS_CHOICES = [
        ('PENDING','PENDING'),
        ('APPROVED','APPROVED'),
        ('REJECTED','REJECTED'),
    ]



    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    reason = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    leave_type = models.CharField(choices=LEAVE_TYPE_CHOICES, max_length=7)
    created_at = models.DateTimeField(auto_now_add=True)



    def clean(self):

        if self.end_date < self.start_date:
            raise ValidationError("End data cannot be before start date.")

        if self.start_date < timezone.now().date():
            raise ValidationError("Cannot apply leave request for past date.")


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submitted_by} - {self.leave_type}"


