from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from rest_framework import status
from app.api import views as api_views
from app.models import Course


class TestUrls(APITestCase):

    def test_course(self):
        url = reverse("api_course")
        self.assertEqual(resolve(url).func.view_class, api_views.CourseView)

    def test_course_details(self):
        url = reverse("api_course_details", kwargs={"id": 1})
        self.assertEqual(resolve(url).func.view_class, api_views.CourseViewDetails)
