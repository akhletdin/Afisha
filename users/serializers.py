from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from . import models


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserCreateSerializer(UserBaseSerializer):

    confirmation_code = serializers.CharField(read_only=True)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        confirmation_code = models.ConfirmationCode.objects.create(user=user)
        confirmation_code.generate_code()
        confirmation_code.save()
        user.confirmation_code = confirmation_code.code  # assign the code to the user
        return user
