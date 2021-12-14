import django_filters
from schools.models import School

class SchoolFilter(django_filters.FilterSet):
    school_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = School
        fields = ['school_name', 'class_offered', 'board', 'co_ed_status']