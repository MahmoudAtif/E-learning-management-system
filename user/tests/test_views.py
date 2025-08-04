from django.test import TestCase, Client
from django.urls import reverse, resolve


class TestView(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.login_page_url = reverse('login_page')
        self.login_url = reverse('login_func')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')

    def test_login_page_func(self):
        response = self.client.get(
            self.login_page_url, HTTP_ACCEPT='application/json')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        print('test_login_page_func --- DONE')

    # def test_login_func(self):
    #     # follow --> the client will follow any redirects
    #     response = self.client.post(
    #         self.login_url, {'username': 'admin', 'password': 'admin'}, follow=True)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertRedirects(response, '/')
    #     # self.client.login(username='admin',password='admin')
    #     print('test_login_func --- DONE')

    def test_register_func(self):
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code, 200)
        # test the template comes form response in exactly the same
        self.assertTemplateUsed(response, 'register.html')
        # test data in in context
        self.assertIsNotNone(response.context['form'])

        print('test_register_func --- DONE')

    def test_logout_func(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEquals(response.status_code, 200)
        print('test_logout_func --- DONE')

    def test_profile_func(self):
        response = self.client.get(self.profile_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        print('test_profile_func --- DONE')
