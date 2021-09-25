from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.CmsDashboard.as_view(), name="cms_dashboard"),
    path('upload-csv', views.UploadCsv.as_view(), name="upload_csv"),
]