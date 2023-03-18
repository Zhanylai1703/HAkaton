from django.urls import path
from .views import (ReportListView, ReportDetail, 
                    ReportExportView, ReportCreateView, 
                    LastWeekReportView, UserReportView)

urlpatterns =[
    path('reports/', ReportListView.as_view()),
    path('report/<int:pk>/', ReportDetail.as_view()),
    path('save/<int:department_id>/', ReportExportView.as_view()),
    path('report/', ReportCreateView.as_view()),
    path('lastweek/', LastWeekReportView.as_view()),
    path('user-reports/', UserReportView.as_view())
   
]