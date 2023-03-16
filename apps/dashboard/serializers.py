from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'user',
            'department',
            'last_week',
            'current_week',
            'next_week',
            'deadline',
            'created_at',
            'updated_at',
        )