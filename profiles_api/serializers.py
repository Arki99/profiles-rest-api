from unittest.util import _MAX_LENGTH
from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing out APIView"""
    name = serializers.CharField(max_length=10)