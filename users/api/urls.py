from django.urls import path,include
from .views import RegistrationView,DepartmentViewSet,LoginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'departments', DepartmentViewSet, basename='department')


urlpatterns = [
    path("", include(router.urls)),
    path('login/',LoginView.as_view(),name='login'),
    path('register/', RegistrationView.as_view(), name='register-employee'),

]