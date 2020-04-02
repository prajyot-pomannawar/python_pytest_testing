from rest_framework import serializers
from .models import Book, User, Log
from rest_framework.response import Response
from rest_framework import status
from .factories import BookFactory, UserFactory


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = "__all__"


class BookFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookFactory
        fields = '__all__'

"""
class UserFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFactory
        fields = '__all__'
        """



