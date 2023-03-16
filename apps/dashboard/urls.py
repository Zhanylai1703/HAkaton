from django.urls import path
from .views import ReportList, ReportDetail, ReportExportView

urlpatterns =[
    path('reports/', ReportList.as_view()),
    path('report/<int:pk>/', ReportDetail.as_view()),
    path('save/', ReportExportView.as_view())
   
]