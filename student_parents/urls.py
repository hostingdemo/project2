from django.urls import path
from django.views.generic.base import TemplateView
from .views import *
from . import views

urlpatterns = [
    path('dashboard/', views.home, name='my_account'),

    # Manage child
    path('manage-child/', views.ManageChild.as_view(), name="manage_child"),
    path('add-child/', views.ChildCreateView.as_view(), name='create_child'),
    path('update-child/<int:pk>', views.ChildUpdateView.as_view(), name='update_child'),
    path('delete-child/<int:pk>', views.ChildDeleteView.as_view(), name='delete_child'),
    
    # common form
    path('common-form/', views.CommonFormView.as_view(), name='common_form_view'),
    path('common-form/create/child/<int:pk>', views.CommonFormCreateOrUpdate.as_view(), name='common_form_create'),

    #profile
    path('profile/', views.profile, name='profile'),
    path('profile/update/<int:pk>', views.profile_update, name='profile-update'),
]
