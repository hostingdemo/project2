from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('dashboard/', views.SchoolDashboard.as_view(), name="school_dashboard"),
    path('info/', views.SchoolInfoCreateOrUpdate.as_view(), name="school_info"),
    path('facilities/', views.SchoolFacilitiesCreateOrUpdate.as_view(), name="school_facilities"),

    # Student Applications
    path('applications/', views.SomeView.as_view(), name="applications"),
    path('applications/?json', views.SomeView.as_view(), name="applications_json"),
    path('student-application/', views.StudentApplicationsAjax.as_view(), name="student_applications"),

    #school fee
    path('school-fee-add/', views.SchoolFeesView.as_view(), name="school_fee_add"),
    path('school-fee-delete/', views.SchoolFeeDelete.as_view(), name="school_fee_delete"),

    #hall of fame
    path('school-fame/', views.SchoolFameView.as_view(), name="school_fame"),
    path('school-fame-add/', views.HallofFameAdd.as_view(), name="school_fame_add"),
    path('school-fame-delete/', views.HallofFameDelete.as_view(), name="school_fame_delete"),

    #school gallery
    path('school-gallery/', views.SchoolGalleryView.as_view(), name="school_gallery"),
    path('school-gallery/delete/<int:pk>', views.delete_img, name="school_img_del"),

    #school logo
    path('school-logo/', views.set_school_logo, name="school_logo"),
    path('school-logo/delete/<int:pk>', views.delete_school_logo, name="school_logo_del"),
]