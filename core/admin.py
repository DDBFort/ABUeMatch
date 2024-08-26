from django.contrib import admin
from .models import Project, Mentor, MentorshipArea


class MentorAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = (
        "first_name",
        "last_name",
        "industry_expertise",
        "years_of_experience",
        "availability",
    )

    # Add search functionality
    search_fields = ("first_name", "last_name", "industry_expertise", "email")

    # Add filters
    list_filter = ("industry_expertise", "years_of_experience", "availability")

    # Group related fields in sections
    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "Professional Details",
            {
                "fields": (
                    "industry_expertise",
                    "years_of_experience",
                    "company",
                    "job_title",
                    "mentorship_areas",
                )
            },
        ),
        (
            "Additional Information",
            {"fields": ("bio", "linkedin_profile", "profile_picture", "availability")},
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # Make timestamps read-only
    readonly_fields = ("created_at", "updated_at")


class ProjectAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = ("title", "user", "status", "start_date", "end_date")

    # Add search functionality
    search_fields = ("title", "description", "user__username", "category")

    # Add filters
    list_filter = ("status", "start_date", "category")

    # Group related fields in sections
    fieldsets = (
        (
            "Project Information",
            {"fields": ("user", "title", "description", "status", "category", "logo")},
        ),
        ("Key Dates", {"fields": ("start_date", "end_date")}),
        (
            "Additional Details",
            {"fields": ("budget", "collaborators", "mentorship", "project_files")},
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    # Make timestamps read-only
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(MentorshipArea)


# Register your models here.
