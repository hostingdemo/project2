from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.CmsDashboard.as_view(), name="cms_dashboard"),
    path('employee-dashbaord', views.UploadCsv.as_view(), name="employee_dashbaord"),

    path('school-info/<school_id>', views.employee_school_info, name="employee_school_info"),
    path('school-facilities/<school_id>', views.school_facilities, name="employee_school_facilities"),

    #school fee
    path('school-fee-add/<school_id>', views.SchoolFeesView.as_view(), name="employee_school_fee_add"),
    path('school-fee-delete/', views.SchoolFeeDelete.as_view(), name="employee_school_fee_delete"),


    path('school-fame/<school_id>', views.SchoolFameView.as_view(), name="employee_school_fame"),
    path('school-fame-add/<school_id>', views.HallofFameAdd.as_view(), name="employee_school_fame_add"),
    path('school-fame-delete/', views.HallofFameDelete.as_view(), name="employee_school_fame_delete"),
]