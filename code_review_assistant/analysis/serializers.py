from rest_framework import serializers


class CodeAnalysisSerializer(serializers.Serializer):
    code = serializers.CharField()
