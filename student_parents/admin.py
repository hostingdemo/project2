from django.contrib import admin

from student_parents.models import (
    Student, 
    ContactDetails,
    ParentDetails, 
    AdditionalDetails,
    Documents
)

admin.site.register(Student)
admin.site.register(ContactDetails)
admin.site.register(ParentDetails)
admin.site.register(AdditionalDetails)
admin.site.register(Documents)