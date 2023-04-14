from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.response import Response

import xlwt

from apps.users.models import Department
from .models import Report
from .serializers import ReportSerializer


class ReportListView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny ,]


class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = []

    def perform_create(self, serializer):
        user = self.request.user
        department_id = serializer.validated_data['department'].id
        if user not in Department.objects.get(id=department_id).user.all():
            raise PermissionDenied('You do not have permission to create a report for this department.')
        serializer.save(user=user)


class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny ,]


class LastWeekReportView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = ()

    def get(self, request):
        today = timezone.now().date()
        last_week_start = today - timezone.timedelta(days=today.weekday() + 7)
        last_week_end = last_week_start + timezone.timedelta(days=6)
        reports = Report.objects.filter(sent=True, week_start_date__gte=last_week_start, week_start_date__lte=last_week_end)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class ReportExportView(APIView):
    permission_classes = [IsAdminUser]
    

    def get(self, request, department_id, format=None):
        department = get_object_or_404(Department, id=department_id)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="report_{department.name}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Report')


        row_num = 0
        columns = ['User', 'Department', 'week_start_date', 'Last Week', 'Current Week', 'Next Week', 'Deadline', 'sent' ]
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)


        rows = Report.objects.filter(department=department).values_list('user__username', 'department__name', 'week_start_date', 'last_week', 'current_week', 'next_week', 'deadline', 'sent')
        for row in rows:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, str(cell_value))

        wb.save(response)
        return response


class UserReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_reports = Report.objects.filter(user=request.user)
        serializer = ReportSerializer(user_reports, many=True)
        return Response(serializer.data)




