from django.contrib import admin

from schools.models import (
    HallofFame,
    SchoolFacilities,
    SchoolFee,
    SchoolGallery,
    SchoolRegistration,
    SchoolReviews,
    SchoolDetail, 
    School
)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'school', 'rating', 'comment' ,'status', 'created_at']
    list_filter = ['status']
    readonly_fields = ('user', 'school', 'rating', 'comment', 'created_at', 'updated_at')

admin.site.register(School)
admin.site.register(SchoolDetail)
admin.site.register(SchoolFacilities)
admin.site.register(HallofFame)
admin.site.register(SchoolGallery)
admin.site.register(SchoolFee)
admin.site.register(SchoolReviews, ReviewAdmin)
admin.site.register(SchoolRegistration)