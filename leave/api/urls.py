from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeLeaveRequestViewSet

router = DefaultRouter()

router.register(r'employee/leave-requests',
                EmployeeLeaveRequestViewSet,
                basename='employee-leave-request'
                )

urlpatterns = [
    path('', include(router.urls)),

]