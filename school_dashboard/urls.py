from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="school_dashboard"),
    path('school-info/', views.school_info, name="school_info"),
    path('school-facilities/', views.school_facilities, name="school_facilities"),

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