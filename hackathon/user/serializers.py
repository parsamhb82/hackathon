from rest_framework import serializers

from django.contrib.auth.models import User
from django.db import transaction
from user.models import UserProfile

class CreateUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    profile_picture = serializers.ImageField(write_only = True, required = False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone_number", "first_name", "last_name", "profile_picture"]

    def create(self, validated_data):
        phone_number = validated_data.pop("phone_number")
        profile_picture = validated_data.pop("profile_picture", None)

        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user, 
                                       phone_number=phone_number, 
                                       profile_picture=profile_picture)
        return user

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value