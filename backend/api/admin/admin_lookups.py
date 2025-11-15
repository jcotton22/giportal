from django.contrib import admin
from api.models import OrganSystem, StaffUploader

@admin.register(OrganSystem)
class OrganSystemAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(StaffUploader)
class StaffUploaderAdmin(admin.ModelAdmin):
    search_fields = ('name',)
