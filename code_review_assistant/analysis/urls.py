from django.urls import path
from .views import analyze_code_view

urlpatterns = [
    path('analyze/', analyze_code_view, name='analyze-code'),
]
