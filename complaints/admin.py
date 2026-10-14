from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "citizen", "category", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "village_location", "citizen__username")
    readonly_fields = ("created_at", "updated_at")
