from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .utils import send_email
from .models import Project

# @receiver(post_save, sender=Project)
# def send_mentor_assignment_email(sender, instance, created, **kwargs):
#     # Check if the mentorship field is set (assigned) and not blank
#     if instance.mentorship:
#         mentor = instance.mentorship  # Get the mentor object
#         project = instance  # Get the project object

#         # Send email to the mentor
#         send_mail(
#             subject=f"You have been assigned to mentor the project: {project.title}",
#             message=f"Dear {mentor.first_name} {mentor.last_name},\n\n"
#                     f"You have been assigned to mentor the project '{project.title}'. "
#                     f"Here are the details of the project:\n\n"
#                     f"Title: {project.title}\n"
#                     f"Description: {project.description}\n"
#                     f"Status: {project.status}\n"
#                     f"Start Date: {project.start_date}\n"
#                     f"End Date: {project.end_date}\n\n"
#                     f"Best regards,\n"
#                     f"The Team",
#             from_email='your_email@example.com',
#             recipient_list=[mentor.email],
#             fail_silently=False,
#         )


@receiver(post_save, sender=Project)
def send_mentor_email(sender, instance, created, **kwargs):
    if instance.mentorship:
        mentor = instance.mentorship
        project = instance

        send_email(
            mentor.email,
            "You've been assigned to a project",
            "mails/mentor.html",
            {"project" : project, "mentor" : mentor},
        )

        send_email(
            project.user.email,
            "Mentor assigned to your project",
            "mails/project.html",
            {"project_owner" : project, "mentor" : mentor},
        )


