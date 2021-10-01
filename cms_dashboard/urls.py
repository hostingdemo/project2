from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.CmsDashboard.as_view(), name="cms_dashboard"),
    path('upload-csv', views.UploadCsv.as_view(), name="upload_csv"),
    path('employee_dashbaord', views.employee_dashbaord, name="employee-employee_dashbaord"),
    path('detail_view/<school_id>', views.detail_view, name="detail_view1212"),

]