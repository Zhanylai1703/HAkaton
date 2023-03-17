from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics
import xlwt

from .models import Report
from .serializers import ReportSerializer

from django.http import HttpResponse


class ReportListView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny ,]

class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = []



class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny ,]



class ReportExportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Report')


        row_num = 0
        columns = ['User', 'Department', 'Last Week', 'Current Week', 'Next Week', 'Deadline', 'sent' ]
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)


        rows = Report.objects.all().values_list('user__username', 'department__name', 'last_week', 'current_week', 'next_week', 'deadline', 'sent')
        for row in rows:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, str(cell_value))

        wb.save(response)
        return response




