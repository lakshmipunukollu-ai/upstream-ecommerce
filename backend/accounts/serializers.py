from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, DistrictProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'tokens']
        read_only_fields = ['id', 'tokens']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'email']


class DistrictProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictProfile
        fields = [
            'id', 'district_name', 'state', 'student_count',
            'ell_percentage', 'free_reduced_lunch_pct',
            'grade_levels_served', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
