from rest_framework import serializers
from accounts.models import CustomUser
from core.models import Company
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": (
            "No account exists with these credentials, check password and email"
        )
    }

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data
        data.update(
            {
                "user": {
                    "email": self.user.email,
                    "username": self.user.username,
                    "id": self.user.id,
                    "is_staff": self.user.is_staff,
                }
            }
        )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Leave empty if no change needed",
        min_length=8,
        style={"input_type": "password", "placeholder": "Password"},
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "id",
            "is_staff",
            "password",
            "access",
            "refresh",
        )

    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = (str(refresh.access_token),)
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class ListCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "firstName",
            "lastName",
            "is_staff",
        )


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = "__all__"