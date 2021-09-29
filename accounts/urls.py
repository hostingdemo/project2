from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    #urls for parents/student
    path('student/login/', views.login_view, name='login'),
    path('signup/', views.signup_student, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    #school urls
    path('school/registration/', views.school_registration,name="school_registration"),
    path('school/school-requests/', views.SchoolRequests.as_view(),name="school_requests"),
    path('school/send_school_activation_mail<uid>', views.send_school_activation_mail,name="send_school_activation_mail"),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'), #url for activate account

    path('create_employee/', views.create_employee, name='create_employee'),   


    #urls for password rest
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'), name='password_reset_complete'),   


]