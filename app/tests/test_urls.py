from django.test import TestCase
from django.urls import reverse, resolve
from app import views


class TestUrl(TestCase):

    def test_home_url(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func, views.home)
        print("test_home_url --> DONE")

    def test_courses_url(self):
        url = reverse("courses")
        self.assertEqual(resolve(url).func, views.courses)
        print("test_courses_url --> DONE")

    def test_filter_data_url(self):
        url = reverse("filter-data")
        self.assertEqual(resolve(url).func, views.filter_data)
        print("test_filter_data_url --> DONE")

    def test_search_url(self):
        url = reverse("search")
        self.assertEqual(resolve(url).func, views.search)
        print("test_search_url --> DONE")

    def test_enrolled_free_course_url(self):
        url = reverse("enrolled_free_course", args=["some-slug"])
        self.assertEqual(resolve(url).func, views.enrolled_free_course)
        print("test_search_url --> DONE")
