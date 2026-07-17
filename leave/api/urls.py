from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeLeaveRequestViewSet, ManagerLeaveRequestViewSet

router = DefaultRouter()

router.register(r'employee/leave-requests',
                EmployeeLeaveRequestViewSet,
                basename='employee-leave-request'
                )

router.register( r'manager/leave-requests',
                 ManagerLeaveRequestViewSet,
                 basename='manager-leave-request'
                 )

urlpatterns = [
    path('', include(router.urls)),

]