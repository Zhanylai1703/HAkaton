from rest_framework import serializers
from apps.dashboard.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'user',
            'department',
            'week_start_date',
            'last_week',
            'current_week',
            'next_week',
            'deadline',
            'created_at',
            'updated_at',
        )


    