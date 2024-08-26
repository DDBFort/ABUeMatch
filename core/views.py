from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .models import Project, Mentor
from datetime import datetime
from django.contrib import messages


def login(request):
    user = request.user

    if user.is_authenticated:
        return redirect("dashboard")

    context = {
        "title": "Login",
    }
    if request.method == "POST":
        username = request.POST["username"]  # Requesting Username
        password = request.POST["password"]  # Requesting Password

        user = auth.authenticate(username=username, password=password)

        if user is not None:  # Cheking If User Exists in the database
            auth.login(request, user)  # Logs in User
            ctx = {"user": username, "date": datetime.now()}
            message = get_template("mails/mail2.html").render(ctx)
            msg = EmailMessage(
                "Login on your account",
                message,
                "The InnoMatch Team",
                [user.email],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            return redirect("dashboard")  # Redirects to home view
        else:
            messages.error(
                request, "Invalid Username or Password"
            )  # Conditional Checking if credentials are correct
            return redirect("login")  # Redirects to login if invalid

    else:
        return render(request, "login.html", context)


def register(request):
    user = request.user

    if user.is_authenticated:
        return redirect("dashboard")

    context = {
        "title": "Sign Up",
    }
    if request.method == "POST":
        # Requesting POST data
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["pass"]
        password2 = request.POST["pass2"]

        # Condition is executed if both passwords are the same
        if password == password2:
            if User.objects.filter(
                email=email
            ).exists():  # Checking databse for existing data
                messages.error(
                    request, "This email is already in use"
                )  # Returns Error Message
                return redirect(register)
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username Taken")
                return redirect("register")

            # Else condition executed if the above conditions are not fulfilled
            else:
                ctx = {"user": username}
                message = get_template("mails/mail.html").render(ctx)
                msg = EmailMessage(
                    "Welcome to InnoMatch",
                    message,
                    "David from Innomatch",
                    [email],
                )
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.save()
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)  # Logs in USER

            # Create user model and redirect to edit-profile
            return redirect("dashboard")
        else:
            messages.info(request, "Passwords do not match")
            return redirect("register")

    else:
        return render(request, "register.html", context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect("login")


def index(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    context = {"title": "Dashboard"}
    return render(request, "dashboard.html", context)


@login_required
def create_project(request):
    if request.method == "POST":
        # Get form data
        title = request.POST.get("title")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        category = request.POST.get("category")
        budget = request.POST.get("budget")
        project_files = request.FILES.get("project_files")

        # Create new project with controlled fields
        new_project = Project.objects.create(
            user=request.user,
            title=title,
            description=description,
            status="Draft",  # Set default status
            start_date=start_date,
            end_date=end_date if end_date else None,
            category=category,
            budget=budget if budget else None,
            mentorship=None,  # Set mentorship to None or assign it later in the admin
            project_files=project_files if project_files else None,
        )

        # Set default collaborators (e.g., empty or controlled by admin later)
        new_project.collaborators.set([])  # No collaborators at the time of submission

        # Save the project
        new_project.save()

        # Success message and redirect
        messages.success(
            request,
            "Your project has been submitted successfully, once our team reviews your work and approves it, they'll assign a mentor best suited for your project. Goodluck😊!",
        )
        return redirect("add-project")  # Change to your actual project list page

    # GET request (show the form)
    context = {
        "title": "Create a New Project",
    }
    return render(request, "create_project.html", context)


@login_required
def projects(request):
    projects = Project.objects.all()
    context = {"projects": projects, "title": "Projects"}
    return render(request, "projects.html", context)


@login_required
def my_projects(request):
    projects = Project.objects.filter(user=request.user)
    context = {"projects": projects, "title": "My Projects"}
    return render(request, "my_projects.html", context)


@login_required
def project_details(request, pk):
    project = Project.objects.get(id=pk)
    context = {
        "project": project,
        "first_name": project.user.first_name,
        "last_name": project.user.last_name,
        "title": f"{project.title}",
    }
    return render(request, "project_details.html", context)


@login_required
def mentors(request):
    mentors = Mentor.objects.filter(availability="Available")
    context = {"mentors": mentors, "title": "Mentors"}
    return render(request, "mentors.html", context)


@login_required
def mentor_details(request, pk):
    mentor = Mentor.objects.get(id=pk)
    mentorship_areas = mentor.mentorship_areas.all()
    mentored_projects = mentor.mentored_projects.all()
    context = { "mentor": mentor, "title": mentor.first_name + " " + mentor.last_name, "mentorship_areas" : mentorship_areas, "mentored_projects" : mentored_projects }
    return render(request, "mentor_details.html", context)


# Create your views here.
