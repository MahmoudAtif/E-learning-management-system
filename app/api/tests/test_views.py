from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from app.models import Course
from user.models import User


class TestView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.course = Course.objects.all().first()
        # self.client=APIClient()

        # if you use token authentication
        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # self.token = Token.objects.create(user=self.user)
        self.course_url = reverse("api_course")
        self.course__details_url = reverse("api_course_details", kwargs={"id": 1})

    def test_course_view(self):
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_view_details(self):
        # to make authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.course__details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
