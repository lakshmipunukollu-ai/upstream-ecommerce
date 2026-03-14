from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, DistrictProfile
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    DistrictProfileSerializer,
    LoginSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
    )
    if not user:
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class DistrictProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DistrictProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = DistrictProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'district_name': '', 'state': ''}
        )
        return profile
