from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Core Application Views
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("add/project/", views.create_project, name="add-project"),
    path("projects/", views.projects, name="projects"),
    path("me/projects/", views.my_projects, name="my-projects"),
    path("project/details/<int:pk>/", views.project_details, name="project-details"),
    path("mentors/", views.mentors, name="mentors"),
    path("mentor/details/<int:pk>/", views.mentor_details, name="mentor-details"),
    # Password Reset Views
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_success/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    # login and sigup views
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
]
