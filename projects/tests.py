from django.test import TestCase, Client

from .models import Project


# Create your tests here.
class ProjectModelTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Test Project",
            description="This is a test project",
        )

    def test_model_setup(self):
        self.assertIsInstance(self.project, Project)
        self.assertEqual(self.project.slug, "test-project")
        self.assertEqual(str(self.project), "Test Project")
        

class ProjectURLTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.project_1 = Project.objects.create(
            name="Test Project",
            description="This is a test project",
        )
        self.project_2 = Project.objects.create(
            name="Test Project 2",
            description="This is a test project 2",
        )

    def test_project_list_url(self):
        response = self.client.get("/projects/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["projects"]), 2)
        self.assertQuerysetEqual(response.context["projects"], Project.objects.all())

    def test_project_create_url(self):
        data = {
            "name": "Test Project 3",
            "description": "This is a test description",
            "project_url": "https://example.com/",
            "tags": "test, project",
            "client": ""
        }

        response = self.client.post("/projects/add-new/", data)

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Project.objects.get(slug="test-project-3"))