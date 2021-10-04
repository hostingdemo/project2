import django_tables2 as tables
from .models import Application

class ApplicationTable(tables.Table):
    class Meta:
        model = Application
        template_name = "django_tables2/bootstrap.html"
        fields = ("application_id", "student_name", "child.gender", "child.user.mobile_no", "child.class_standard", "child.date_of_birth", "created_at",)