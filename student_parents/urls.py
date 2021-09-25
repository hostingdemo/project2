from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('dashboard/', views.home, name='my_account'),
    path('dashboard/school', views.school_dashboard, name='school_dashboard'),
    path('student-list', views.student_list, name='sd'),
    path('detail-view/<student_id>', views.detail_view, name='detail_view'),
    path('register-child/', views.Registerchild, name='register_child'),
    path('register-student/', views.RegisterStudent, name='register_student'),
    path('update/<student_id>', views.UpdateRegisterStudent, name='update'),
    path('delete/<student_id>', views.Delete, name='delete'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/<int:pk>', views.profile_update, name='profile-update'),
    path('jsoncall/',views.jsoncall,name='jsoncall'),
]
