from django.test import TestCase
from django.urls import resolve, reverse
from user import views


class TestUrl(TestCase):

    def test_login_page_url(self):
        url = reverse("login_page")
        self.assertEquals(resolve(url).func, views.login_page)
        print("test_login_page_url ---> DONE")

    def test_login_func_url(self):
        url = reverse("login_func")
        self.assertEquals(resolve(url).func, views.login_func)
        print("test_login_func_url ---> DONE")

    def test_register_url(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, views.register)
        print("test_register_url ---> DONE")

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, views.logout_page)
        print("test_logout_url ---> DONE")

    def test_profile_url(self):
        url = reverse("profile")
        self.assertEquals(resolve(url).func, views.profile)
        print("test_profile_url ---> DONE")
