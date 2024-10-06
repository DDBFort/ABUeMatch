from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import MentorshipArea, Mentor, Project
from datetime import date

User = get_user_model()


class MentorshipAreaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mentorship_area = MentorshipArea.objects.create(area="Software Development")

    def test_mentorship_area_str(self):
        self.assertEqual(str(self.mentorship_area), "Software Development")

    def test_unique_area(self):
        with self.assertRaises(Exception):
            MentorshipArea.objects.create(area="Software Development")


class MentorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.mentorship_area = MentorshipArea.objects.create(area="Data Science")
        cls.mentor = Mentor.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            industry_expertise="Data Science",
            years_of_experience=10,
            company="Tech Inc.",
            job_title="Senior Data Scientist",
            bio="Experienced Data Scientist",
            linkedin_profile="http://linkedin.com/in/johndoe",
            availability="Available",
        )
        cls.mentor.mentorship_areas.add(cls.mentorship_area)

    def test_mentor_str(self):
        self.assertEqual(str(self.mentor), "John Doe - Data Science")

    def test_mentor_email_unique(self):
        with self.assertRaises(Exception):
            Mentor.objects.create(
                first_name="Jane",
                last_name="Doe",
                email="john.doe@example.com",
                industry_expertise="Data Science",
                years_of_experience=5,
            )

    def test_mentor_mentorship_areas(self):
        self.assertIn(self.mentorship_area, self.mentor.mentorship_areas.all())


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.mentor = Mentor.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            industry_expertise="Cybersecurity",
            years_of_experience=8,
            availability="Available",
        )
        cls.project = Project.objects.create(
            user=cls.user,
            title="AI Development",
            description="An AI project",
            status="In Progress",
            start_date=date(2023, 1, 1),
            category="Artificial Intelligence",
            budget=5000.00,
            mentorship=cls.mentor,
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "AI Development")

    def test_project_user(self):
        self.assertEqual(self.project.user.username, "testuser")

    def test_project_status_choices(self):
        self.project.status = "Completed"
        self.project.save()
        self.assertEqual(self.project.status, "Completed")

    def test_project_collaborators(self):
        collaborator = User.objects.create_user(username="collab", password="password")
        self.project.collaborators.add(collaborator)
        self.assertIn(collaborator, self.project.collaborators.all())

    def test_project_mentorship(self):
        self.assertEqual(self.project.mentorship, self.mentor)
