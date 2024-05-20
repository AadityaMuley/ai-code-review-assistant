# analysis/views.py
from django.shortcuts import render  # noqa: F401

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CodeAnalysisSerializer
from src.main import analyze_code, generate_code_review_comments  # Import your existing functions


@api_view(['POST'])
def analyze_code_view(request):
    serializer = CodeAnalysisSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['code']
        analysis_result = analyze_code(code)
        review_comments = generate_code_review_comments(code)
        return Response({
            'analysis': analysis_result,
            'comments': review_comments
        })
    return Response(serializer.errors, status=400)
