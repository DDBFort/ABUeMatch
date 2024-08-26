from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MentorshipArea(models.Model):
    area = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.area


class Mentor(models.Model):
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Professional Details
    industry_expertise = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    # Additional Information
    bio = models.TextField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="mentors/", blank=True, null=True)

    # Availability
    availability = models.CharField(
        max_length=100,
        choices=[("Available", "Available"), ("Not Available", "Not Available")],
    )

    # Mentorship Areas
    mentorship_areas = models.ManyToManyField(MentorshipArea)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.industry_expertise}"


class Project(models.Model):
    # Project Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("Draft", "Draft"),
            ("Submitted", "Submitted"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
        ],
    )
    logo = models.ImageField(upload_to="projects/pfps", default="project_default.jpg")

    # Key Dates
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    # Additional Details
    category = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    collaborators = models.ManyToManyField(
        User, related_name="collaborated_projects", blank=True
    )
    mentorship = models.ForeignKey(
        Mentor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="mentored_projects",
    )

    # Files and Resources
    project_files = models.FileField(upload_to="projects/", blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Create your models here.
