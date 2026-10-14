from django.conf import settings
from django.db import models

class Complaint(models.Model):
    class Category(models.TextChoices):
        ROADS = "Roads", "Roads"
        WATER = "Water Supply", "Water Supply"
        ELECTRICITY = "Streetlights/Electricity", "Streetlights/Electricity"
        DRAINAGE = "Drainage", "Drainage"
        SANITATION = "Sanitation", "Sanitation"
        OTHER = "Other", "Other"

    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        IN_PROGRESS = "In Progress", "In Progress"
        RESOLVED = "Resolved", "Resolved"

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="complaints"
    )
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=40, choices=Category.choices)
    village_location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="complaint_images/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    official_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} - {self.title}"
