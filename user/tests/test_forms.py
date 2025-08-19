from django.test import TestCase
from user.forms import CreateUserForm, UserChangeForm


class TestForm(TestCase):
    def test_create_user_form(self):
        form = CreateUserForm(
            data={
                "username": "test2",
                "email": "test2@gmail.com",
                "password1": "test123456789aaaaaaaaa",
                "password2": "test123456789aaaaaaaaa",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_change_form(self):
        form = UserChangeForm(
            data={
                "username": "test",
                "first_name": "test",
                "last_name": "test",
                "email": "test@gmail.com",
            }
        )
        self.assertTrue(form.is_valid())
