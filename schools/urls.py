from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('explore/', views.SchoolListView.as_view(), name='explore'),
    path('explore/compare-schools/', views.compare_schools, name='compare_schools'),
    path('explore/school/<int:pk>', views.SchoolDetailView.as_view(), name='school_details'),
    
    # review urls
    path('explore/school/<int:pk>/reviews/', views.get_school_reviews, name='school_reviews'),
    path('explore/school/<int:pk>/reviews/delete/<int:reviewId>', views.delete_school_reviews, name='delete_review'),
]