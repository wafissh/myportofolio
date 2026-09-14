from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, TechStack, Project, Education


class MainViewTest(TestCase):
    def setUp(self):
        self.tech = TechStack.objects.create(name="Django", category="BACKEND")
        self.project = Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            role="Fullstack Developer",
            description="My personal portfolio website.",
            thumbnail="https://example.com/thumb.png",
            is_featured=True,
        )
        self.project.tech_stacks.add(self.tech)
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            is_featured=True,
        )
        self.education = Education.objects.create(
            title="S1 Sistem Informasi",
            education_loc="Universitas Indonesia",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_data_models_appear_in_html(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, self.education.title)
        self.assertContains(response, self.education.education_loc)
        self.assertContains(response, self.tech.name)

    def test_empty_state_when_no_data(self):
        Project.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()
        TechStack.objects.all().delete()
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "On searching for this project")


class ExperienceViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

    def test_data_model_appears_in_html(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Present")
        self.assertContains(response, "Back to Home")

    def test_empty_state_when_no_data(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "On searching for this experience")


class TechnologiesViewTest(TestCase):
    def setUp(self):
        self.tech = TechStack.objects.create(
            name="Django",
            category="BACKEND",
            icon_class="devicon-django-plain",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_technologies"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "technologies.html")

    def test_data_model_appears_in_html(self):
        response = self.client.get(reverse("main:show_technologies"))
        self.assertContains(response, self.tech.name)
        self.assertContains(response, self.tech.icon_class)
        self.assertContains(response, "Back to Home")

    def test_empty_state_when_no_data(self):
        TechStack.objects.all().delete()
        response = self.client.get(reverse("main:show_technologies"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tech stack akan ditampilkan di sini")


class ProjectsViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            role="Fullstack Developer",
            description="My personal portfolio website.",
            thumbnail="https://example.com/thumb.png",
        )

    def test_url_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_data_model_appears_in_html(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.role)
        self.assertContains(response, "Back to Home")

    def test_empty_state_when_no_data(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "On searching for this project")


class NonexistentPageTest(TestCase):
    def test_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)
