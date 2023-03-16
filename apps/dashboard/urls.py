from django.urls import path
from .views import ReportListView, ReportDetail, ReportExportView, ReportCreateView

urlpatterns =[
    path('reports/', ReportListView.as_view()),
    path('report/<int:pk>/', ReportDetail.as_view()),
    path('save/', ReportExportView.as_view()),
    path('report/', ReportCreateView.as_view()),
   
]