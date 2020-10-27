from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Book


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """
        Create user and default subscription.
        """
        user = super().create(validated_data)

        user.create_default_subscription()
        return user

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["author", "name", "isbn"]
