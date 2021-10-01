from django.contrib import admin

from student_parents.models import (
    Child,
    CommonForm
)

admin.site.register(Child)
admin.site.register(CommonForm)