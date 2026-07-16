from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.api.permissions import IsManagerOrSuperUser, IsSuperUser
from users.api.serializers import EmployeeRegisterSerializer, LoginSerializer, DepartmentSerializer, \
    ManagerRegisterSerializer
from users.models import Department
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class EmployeeRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):

        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is  None:
            return Response({'message':"Invalid email or password."},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'message':"your account is deactivate."},
                            status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'message': "login successful.",
            'refresh': str(refresh),
            'access': access_token,
        }, status=status.HTTP_200_OK
        )

class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsManagerOrSuperUser]
    lookup_field = 'public_id'

class ManagerRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = ManagerRegisterSerializer
    permission_classes = [IsSuperUser]