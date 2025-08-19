from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from user.models import User
from app import views
from app.models import Course, Author, Category


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.home_url = reverse("home")
        self.user = User.objects.create_user(
            username="test", email="test@gmail.com", password="test"
        )
        self.author = Author.objects.all().first()
        self.category = Category.objects.all().first()
        self.course = Course.objects.all().first()

    def test_home_view(self):
        request = self.factory.get(self.home_url)
        request.user = self.user
        response = views.home(request)
        self.assertEqual(response.status_code, 200)
        print("test_home_view --> DONE")

    def test_courses_view(self):
        url = reverse("courses")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/courses.html")
        print("test_courses_view --> DONE")

    def filter_data_view(self):
        url = reverse("filter-data")
        # response=self.client.get(url)
        request = self.factory.get(url)
        response = views.filter_data(request)
        self.assertEqual(response.status_code, 200)

    def test_course_detail_view(self):
        url = reverse("course_details", args=["some-slug"])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_enrolled_free_course_view(self):
        url = reverse("enrolled_free_course", args=["some-slug"])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
