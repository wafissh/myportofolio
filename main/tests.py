from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User, Group

import json

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

    def test_data_model_appears_in_api(self):
        response = self.client.get(reverse("get_projects_json"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        fields = data[0]["fields"]
        self.assertEqual(fields["title"], self.project.title)
        self.assertEqual(fields["description"], self.project.description)
        self.assertEqual(fields["role"], self.project.role)

    def test_page_contains_static_chrome(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, "Back to Home")
        self.assertContains(response, "Selected Projects")
        self.assertContains(response, "project-search-form")

    def test_empty_state_when_no_data(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")


class AuthorizationTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            description="My personal portfolio website.",
        )
        self.admin = User.objects.create_superuser("admin", password="adminpass123")
        self.editor = User.objects.create_user("editor", password="editorpass123")
        self.editor.groups.add(Group.objects.create(name="editor"))
        self.member = User.objects.create_user("member", password="memberpass123")

        self.create_url = reverse("main:create_project")
        self.update_url = reverse("main:update_project", args=[self.project.pk])
        self.delete_url = reverse("main:delete_project", args=[self.project.pk])
        self.star_url = reverse("main:toggle_star", args=[self.project.pk])

    def test_anonymous_redirected_to_login(self):
        for url in (self.create_url, self.update_url, self.delete_url, self.star_url):
            for method in (self.client.get, self.client.post):
                response = method(url)
                self.assertEqual(response.status_code, 302, url)
                self.assertTrue(
                    response.url.startswith("/login/"), response.url
                )

    def test_member_gets_403_on_write_actions(self):
        self.client.force_login(self.member)
        for url in (self.create_url, self.update_url):
            self.assertEqual(self.client.get(url).status_code, 403, url)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)

    def test_editor_can_update_only(self):
        self.client.force_login(self.editor)
        self.assertEqual(self.client.get(self.update_url).status_code, 200)
        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)

    def test_admin_can_create_update_delete(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.create_url).status_code, 200)
        self.assertEqual(self.client.get(self.update_url).status_code, 200)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_templates_hide_action_buttons(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.create_url)
        self.assertNotContains(response, reverse("main:update_project", args=[self.project.pk]))
        self.assertNotContains(response, self.delete_url)
        self.assertNotContains(response, 'CAN_EDIT = "true"')

        self.client.force_login(self.admin)
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, self.create_url)
        self.assertContains(response, 'CAN_EDIT = "true"')

    def test_add_project_modal_only_rendered_for_superuser(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(response, 'id="add-project-modal"')

        self.client.force_login(self.admin)
        response = self.client.get(reverse("main:show_projects"))
        self.assertContains(response, 'id="add-project-modal"')
        self.assertContains(response, 'popovertarget="add-project-modal"')
        self.assertContains(response, 'id="project-form"')


class StarTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            description="My personal portfolio website.",
        )
        self.user = User.objects.create_user("stargazer", password="password123")
        self.star_url = reverse("main:toggle_star", args=[self.project.pk])

    def test_projects_page_renders_star_control(self):
        response = self.client.get(reverse("main:show_projects"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "star-count")

    def test_star_requires_login(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_star_only_accepts_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_star_toggles_and_counts_once_per_user(self):
        self.client.force_login(self.user)

        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 1)
        self.assertIn(self.user, self.project.starred_by.all())

        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 0)
        self.assertNotIn(self.user, self.project.starred_by.all())

    def test_star_is_unique_per_user(self):
        self.project.starred_by.add(self.user)
        self.project.starred_by.add(self.user)
        self.assertEqual(self.project.starred_by.count(), 1)


class ProjectApiTest(TestCase):
    def setUp(self):
        user = User.objects.create_user("someone", password="password123")
        self.project = Project.objects.create(
            title="Portfolio Website",
            slug="portfolio-website",
            role="Fullstack Developer",
            description="My personal portfolio website.",
        )
        self.project.starred_by.add(user)

    def test_api_returns_json(self):
        response = self.client.get(reverse("get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        fields = set(data[0]["fields"])
        self.assertTrue(
            {"title", "slug", "description", "role", "is_featured"} <= fields
        )

    def test_api_does_not_leak_sensitive_fields(self):
        response = self.client.get(reverse("get_projects_json"))
        data = json.loads(response.content)
        fields = set(data[0]["fields"])

        for sensitive in ("password", "starred_by", "last_login", "email", "is_superuser"):
            self.assertNotIn(sensitive, fields)

    def test_api_sends_pagination_headers(self):
        response = self.client.get(reverse("get_projects_json"))
        self.assertEqual(response["X-Total-Pages"], "1")
        self.assertEqual(response["X-Current-Page"], "1")

    def test_api_paginates_results(self):
        for i in range(6):
            Project.objects.create(
                title=f"Proyek Tambahan {i}",
                slug=f"proyek-tambahan-{i}",
                description="Deskripsi singkat.",
            )
        page_one = self.client.get(reverse("get_projects_json"))
        page_two = self.client.get(reverse("get_projects_json") + "?page=2")

        self.assertEqual(len(json.loads(page_one.content)), 6)
        self.assertEqual(len(json.loads(page_two.content)), 1)
        self.assertEqual(page_one["X-Total-Pages"], "2")
        self.assertEqual(page_two["X-Current-Page"], "2")

    def test_api_filters_by_title(self):
        Project.objects.create(
            title="Django REST API",
            slug="django-rest-api",
            description="Proyek uji pencarian.",
        )
        response = self.client.get(reverse("get_projects_json") + "?title=django")
        data = json.loads(response.content)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], "Django REST API")


class CreateProjectAjaxTest(TestCase):
    def setUp(self):
        self.url = reverse("main:create_project_ajax")
        self.admin = User.objects.create_superuser("admin", password="adminpass123")
        self.member = User.objects.create_user("member", password="memberpass123")
        self.valid_data = {
            "title": "Proyek AJAX",
            "slug": "proyek-ajax",
            "role": "Developer",
            "description": "Deskripsi proyek AJAX.",
            "thumbnail": "https://example.com/thumb.png",
            "project_url": "https://example.com",
        }

    def test_anonymous_gets_403_json(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertFalse(Project.objects.exists())

    def test_member_gets_403_json(self):
        self.client.force_login(self.member)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.exists())

    def test_superuser_can_create_project(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.url, self.valid_data)

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn("message", data)
        self.assertTrue(Project.objects.filter(pk=data["pk"]).exists())
        self.assertEqual(Project.objects.get().title, "Proyek AJAX")

    def test_invalid_data_returns_400_with_errors(self):
        self.client.force_login(self.admin)
        invalid_data = {**self.valid_data, "title": "   "}
        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("title", data["errors"])
        self.assertFalse(Project.objects.exists())

    def test_get_not_allowed(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.url).status_code, 405)


class NonexistentPageTest(TestCase):
    def test_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)
